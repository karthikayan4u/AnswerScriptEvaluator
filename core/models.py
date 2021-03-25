from django.db import models
from django.conf import settings

# Create your models here.
class Questions(models.Model):
    question = models.TextField(max_length=250)
    answer = models.TextField(max_length=1000)

class Answers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    question = models.TextField(max_length=250)
    answer = models.TextField(max_length=1000)

class Scores(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    score = models.FloatField()