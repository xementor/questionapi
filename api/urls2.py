from django.urls import path
from . import views2

urlpatterns = [
    path('login/', views2.LoginView.as_view(), name='login'),
    path('questions/', views2.QuestionListView.as_view(), name='questions'),
    path('questions/<pk>/', views2.QuestionDetailView.as_view(), name='question'),
    path('questions/<pk>/', views2.save_comment),

]