from django.shortcuts import get_object_or_404, render, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from .models import CComment, Course, QComment, Question, Student
from .serializers import CComentSerializer, CommentSerializer, CourseSerializer, CreateQuestionSerializer, QuestionSerializer, StudentSerializer

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['semister', 'course_code', 'year', 'term']
    search_fields = ['course_code', 'year']
    ordering_fields = ['course_code', 'year']

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (student, created) = Student.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            questions = Question.objects.filter(student=student)
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        if request.method ==  'POST':
            serializer = QuestionSerializer(data=request.data, context={'user_id' :  request.user.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        

            
        

    

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
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return QComment.objects.filter(question_id=self.kwargs['question_pk'])

    def get_serializer_context(self):
        return {'question_id': self.kwargs['question_pk'], 'user_id': self.request.user.id}


class CommentCommentViewSet(ModelViewSet):
    queryset = CComment.objects.all()
    serializer_class = CComentSerializer

    def get_queryset(self):
        return CComment.objects.filter(comment_id=self.kwargs['comment_pk'])

    def get_serializer_context(self):
        return {'comment_id': self.kwargs['comment_pk'], 'user_id': self.request.user.id}

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (student, created) = Student.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = StudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)


