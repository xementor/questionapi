from django.urls import path
from . import views2

urlpatterns = [
    path('', views2.index),
    path('questions/', views2.QuestionListView.as_view()),
    path('questions/<pk>/', views2.QuestionDetailView.as_view()),
]