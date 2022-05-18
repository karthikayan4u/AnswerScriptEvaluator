from answer_correction.settings import EMAIL_HOST_USER
from django.http.response import HttpResponse
from core.utils import render_to_pdf
from core.models import Answer, Question, Score
from core.forms import GetAnswer
from django.shortcuts import redirect, render
from django.views.generic import View
from core.markcalculation import calc, handle_uploaded_file
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail


def send_email(request, mark):
    messages.info(request, f"Your Final Score has been sent to your registered email!!")
    send_mail(
        "Your Final Score in Answer Evaluator",
        f"""Greetings {request.user.username}!!
After evaluating your answer script, we announce that you have scored {mark} out of 100 in your exam. You are free to reattempt the exam by logging in again to upgrade your mark!
You can also download your recorded answers by logging in again!
With regards
Answer Evaluator Team""",
        EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False,
    )
    logout(request)


def get_score(request):
    score = None
    if request.user.is_authenticated:
        recorded_score = Score.objects.filter(user=request.user)
        if recorded_score.exists():
            score = recorded_score[0].score
    return score

class HomeView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'home.html')

class TeacherView(View):
    def get(self, *args, **kwargs):
        return redirect("/teacher")

class StudentView(View):
    def get(self, *args, **kwargs):
            score = get_score(self.request)
            context = {
                'score':score,
            }
            return render(self.request, 'student.html', context)

class OfflineAnswerView(View):
    def get(self, *args, **kwargs):
            questions = Question.objects.all()
            score = score = get_score(self.request)
            form = GetAnswer()
                
            context = {
                'questions':questions,
                'l': len(questions),
                'score':score,
                'form':form,
            }
            return render(self.request, 'offline.html', context)
    def post(self, *args, **kwargs):
        student = GetAnswer(self.request.POST, self.request.FILES)  
        if student.is_valid() and self.request.FILES['file'].name.split('.')[1] == 'pdf':
            questions = Question.objects.all()
            answers = handle_uploaded_file(self.request.FILES['file'], set(questions))
            marks = 0
            score = Score.objects.filter(user=self.request.user)
            if score.exists():
                for question in questions:
                    answer = answers.get(question.question, ' ')
                    recorded_answers = Answer.objects.filter(user=self.request.user, question = question.question)
                    if recorded_answers:
                        recorded_answers.update(answer = answer)
                    else:
                        Answer.objects.create(user=self.request.user, question = question.question, answer = answer)
                    marks += calc(question.answer, answer)
                mark = int(round((marks / len(questions)) * 100))
                score = score[0]
                score.score = mark 
                score.save()
            else:
                for question in questions:
                    answer = answers.get(question.question, ' ')
                    Answer.objects.create(user=self.request.user, question = question.question, answer = answer)
                    marks += calc(question.answer, answer)
                mark = int(round((marks / len(questions)) * 100))
                Score.objects.create(user=self.request.user, score=mark)
            send_email(self.request, mark)
            return redirect("core:student")
        messages.info(self.request,"Please upload a pdf file!")
        return redirect("core:offline")

class OnlineAnswerView(View):
    def get(self, *args, **kwargs):
            questions = Question.objects.all()
            score = score = get_score(self.request)
                
            context = {
                'questions':questions,
                'l': len(questions),
                'score':score,
            }
            return render(self.request, 'online.html', context)
    def post(self, *args, **kwargs):
            questions = Question.objects.all()
            marks = 0
            score = Score.objects.filter(user=self.request.user)
            if score.exists():
                for p, question in enumerate(questions):
                    answer = self.request.POST.get("q"+str(p + 1))
                    recorded_answers = Answer.objects.filter(user=self.request.user, question = question.question)
                    if recorded_answers:
                        recorded_answers.update(answer = answer)
                    else:
                        Answer.objects.create(user=self.request.user, question = question.question, answer = answer)
                    marks += calc(question.answer, answer)
                mark = int(round((marks / len(questions)) * 100))
                score = score[0]
                score.score = mark 
                score.save()
            else:
                for p, question in enumerate(questions):
                    answer = self.request.POST.get("q"+str(p + 1))
                    Answer.objects.create(user=self.request.user, question = question.question, answer = answer)
                    marks += calc(question.answer, answer)
                mark = int(round((marks / len(questions)) * 100))
                Score.objects.create(user=self.request.user, score=mark)
            send_email(self.request, mark)
            return redirect("core:student")


class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        response = Answer.objects.filter(user=self.request.user)
        score = Score.objects.filter(user=self.request.user)
        #getting the template
        pdf = render_to_pdf('recordedresponse.html', {'responses':response, 'user':self.request.user, 'score':score[0].score})
        #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
