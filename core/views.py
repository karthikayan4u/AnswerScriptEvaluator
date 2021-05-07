from core.models import Answers, Questions, Scores
from core.forms import GetAnswer
from django.shortcuts import redirect, render
from django.views.generic import View
from core.markcalculation import calc
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.

class AnswerView(View):
    def get(self, *args, **kwargs):
            questions = Questions.objects.all()
            score = None
            if self.request.user.is_authenticated:
                score = Scores.objects.filter(user=self.request.user)
                if score.exists():
                    score = score[0].score
                
            context = {
                'questions':questions,
                'l': len(questions),
                'score':score,
            }
            return render(self.request, 'home.html', context)
    def post(self, *args, **kwargs):
            questions = Questions.objects.all()
            marks = 0
            score = Scores.objects.filter(user=self.request.user)
            if score.exists():
                for p, question in enumerate(questions):
                    answer = self.request.POST.get("q"+str(p + 1))
                    Answers.objects.filter(user=self.request.user, question = question.question).update(answer = answer)
                    marks += calc(question.answer, answer)
                mark = round((marks / len(questions)) * 100, 2)
                score = score[0]
                score.score = mark 
                score.save()
            else:
                for p, question in enumerate(questions):
                    answer = self.request.POST.get("q"+str(p + 1))
                    Answers.objects.create(user=self.request.user, question = question.question, answer = answer)
                    marks += calc(question.answer, answer)
                mark = round((marks / len(questions)) * 100, 2)
                Scores.objects.create(user=self.request.user, score=mark)
            messages.info(self.request, f"Your Final Score has been to your registered email")

            send_mail(
                "Your Final Score in Answer Evaluator",
                f"""You have scored {mark} out of 100 in your exam conducted in Answer Evaluator platform. You are free to reattempt the exam to upgrade your mark!

                With regards
                Answer Evaluator Team""",
                "sanjive125@gmail.com",
                [self.request.user.email],
                fail_silently=False,
            )
            logout(self.request)
            return redirect(".")
