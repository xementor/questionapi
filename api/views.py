from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import IsOwnerOfQuestion
from .models import CComment, Course, Like, QComment, Question, Student
from .serializers import CComentSerializer, CommentSerializer, CourseSerializer, LikeSerializer, QuestionSerializer, StudentSerializer

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
        elif self.request.method in  ['PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOfQuestion()]
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

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def like(self,request, pk):
        (student, created) = Student.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            ctype = ContentType.objects.get(model='question')
            already_liked = Like.objects.filter(object_id=pk,student=student,content_type=ctype).count() > 0
            if already_liked:
                return Response('You have already liked this contetn')
            
            Like.objects.create(object_id=pk,student=student,content_type=ctype)
            return Response("you have like this content")

        

            

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return QComment.objects.filter(question_id=self.kwargs['question_pk'])

    def get_serializer_context(self):
        return {'question_id': self.kwargs['question_pk'], 'user_id': self.request.user.id}
    
    def get_permissions(self):
        if self.request.method == permissions.SAFE_METHODS:
            return [AllowAny()]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOfQuestion()]
        return [IsAuthenticated()]


class CommentCommentViewSet(ModelViewSet):
    queryset = CComment.objects.all()
    serializer_class = CComentSerializer

    def get_queryset(self):
        return CComment.objects.filter(comment_id=self.kwargs['comment_pk'])
    
    def get_permissions(self):
        if self.request.method == permissions.SAFE_METHODS:
            return [AllowAny()]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwnerOfQuestion()]
        return [IsAuthenticated()]


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


