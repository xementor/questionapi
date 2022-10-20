from django.shortcuts import get_object_or_404, render, HttpResponse

from api.forms import QuestionCommentForm

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': ['1', '2', '3']}
    return render(request, 'contents.html', context)



from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .models import QComment, Question

class QuestionListView(ListView):
    model = Question


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = int(self.kwargs['pk'])
        context['question'] = Question.objects.get(id=question_id)
        context['comments'] = QComment.objects.filter(question_id=question_id)
        return context

class QuestionCommentFormView(FormView):
    template_name = 'api/comment_form.html'
    form_class = QuestionCommentForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.save_comment()
        return super().form_valid(form)