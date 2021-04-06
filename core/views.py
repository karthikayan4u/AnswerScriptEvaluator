from core.models import Answers, Questions, Scores
from core.forms import GetAnswer
from django.shortcuts import redirect, render
from django.views.generic import View
from core.markcalculation import calc
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.

class AnswerView(View):
    def get(self, *args, **kwargs):
            form  = GetAnswer()
            questions = Questions.objects.all()[:10]
            context = {
                'form':form,
                'question1':questions[0].question,
                'question2':questions[1].question,
                'question3':questions[2].question,
                'question4':questions[3].question,
                'question5':questions[4].question,
                'question6':questions[5].question,
                'question7':questions[6].question,
                'question8':questions[7].question,
                'question9':questions[8].question,
                'question10':questions[9].question,
            }
            return render(self.request, 'home.html', context)
    def post(self, *args, **kwargs):
            
            form = GetAnswer(self.request.POST or None)
            
            if form.is_valid():
                answer1 = form.cleaned_data.get('answer1')
                answer2 = form.cleaned_data.get('answer2')
                answer3 = form.cleaned_data.get('answer3')
                answer4 = form.cleaned_data.get('answer4')
                answer5 = form.cleaned_data.get('answer5')
                answer6 = form.cleaned_data.get('answer6')
                answer7 = form.cleaned_data.get('answer7')
                answer8 = form.cleaned_data.get('answer8')
                answer9 = form.cleaned_data.get('answer9')
                answer10 = form.cleaned_data.get('answer10')
                questions = Questions.objects.all()[:10]
                marks = 0
                score = Scores.objects.filter(user=self.request.user)
                if score.exists():
                    for question, answer in zip(questions, [answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9, answer10]):
                        Answers.objects.filter(user=self.request.user, question = question.question).update(answer = answer)
                        marks += calc(question.answer, answer)
                    mark = round((marks / 10) * 100, 2)
                    score = score[0]
                    score.score = mark 
                    score.save()
                else:
                    for question, answer in zip(questions, [answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8, answer9, answer10]):
                        Answers.objects.create(user=self.request.user, question = question.question, answer = answer)
                        marks += calc(question.answer, answer)
                    mark = round((marks / 10) * 100, 2)
                    Scores.objects.create(user=self.request.user, score=mark)
                messages.info(self.request, f"Your Final Score is {mark}%!")
                logout(self.request)
                return redirect(".")
