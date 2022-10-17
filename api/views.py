from django.shortcuts import get_object_or_404, render, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import CComment, Course, QComment, Question
from .serializers import CComentSerializer, CommentSerializer, CourseSerializer, QuestionSerializer

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['semister', 'course_code', 'year', 'term']
    search_fields = ['course_code', 'year']
    ordering_fields = ['course_code', 'year']

    

class QuestionDetail(ModelViewSet):
    queryset = Question.objects.all()
    
    def get(self, request, id):
        question = get_object_or_404(Question, pk=id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    def put(self, request, id):
        question = get_object_or_404(Question, pk=id)
        serializer = QuestionSerializer(question,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CommentViewSet(ModelViewSet):
    # queryset = QComment.objects.all()
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return QComment.objects.filter(question_id=self.kwargs['question_pk'])

    def get_serializer_context(self):
        return {'question_id': self.kwargs['question_pk']}


class CommentCommentViewSet(ModelViewSet):
    queryset = CComment.objects.all()
    serializer_class = CComentSerializer