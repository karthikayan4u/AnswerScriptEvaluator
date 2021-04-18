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
            questions = Questions.objects.all()
            context = {
                'questions':questions,
                'l': len(questions)
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
                mark = round((marks / 10) * 100, 2)
                score = score[0]
                score.score = mark 
                score.save()
            else:
                for p, question in enumerate(questions):
                    answer = self.request.POST.get("q"+str(p + 1))
                    Answers.objects.create(user=self.request.user, question = question.question, answer = answer)
                    marks += calc(question.answer, answer)
                mark = round((marks / 10) * 100, 2)
                Scores.objects.create(user=self.request.user, score=mark)
            messages.info(self.request, f"Your Final Score is {mark}%!")
            logout(self.request)
            return redirect(".")
