from django.urls import path
from .views import AnswerView
app_name = 'core'

urlpatterns = [
    path('', AnswerView.as_view(), name='home'),
    ]