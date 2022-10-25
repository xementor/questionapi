from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import QComment, Question, Student, User
from .forms import QuestionCommentForm
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages

class QuestionListView(View):
    def get(self, request):
        questions = Question.objects.all()
        context = {}
        context['questions'] = questions
        context['user']  = self.request.user
        print(self.request.user.id)
        return render(request, template_name='api/question_list.html', context=context)


class QuestionDetailView(View):
    def get(self, request,pk):
        question_id = int(self.kwargs['pk'])
        context = {}
        context['question'] = Question.objects.get(id=question_id)
        context['comments'] = QComment.objects.filter(question_id=question_id)
        context['user'] = self.request.user
        return render(request,template_name='api/question_detail.html', context=context)

    def post(self, request, pk):
        # return HttpResponse(self.request.user.id)
        (student, created) = Student.objects.get_or_create(user_id=request.user.id)
        student_id  = student.id
        qc = QComment.objects.create(student_id=student_id, question_id=pk)
        qc.comment = request.POST.get('comment')
        qc.save()
        return redirect('question', pk)


class QuestionCommentFormView(FormView):
    template_name = 'api/comment_form.html'
    form_class = QuestionCommentForm
    success_url = '/thanks/'



def save_comment(request, pk):
    if request.method == "POST":
        return render('api/post.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
        else:
            messages.error(request,"invalid username and password")
        return redirect("/questions/")
