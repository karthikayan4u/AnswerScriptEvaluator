from django.urls import path
from .views import OfflineAnswerView, OnlineAnswerView, HomeView
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('offline', OfflineAnswerView.as_view(), name='offline'),
    path('online', OnlineAnswerView.as_view(), name='online'),
    ]