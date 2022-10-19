from django.shortcuts import get_object_or_404, render, HttpResponse

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': ['1', '2', '3']}
    return render(request, 'contents.html', context)