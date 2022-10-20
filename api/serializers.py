from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import CComment, Course, Like, QComment, Question, Student


class QuestionSerializer(serializers.ModelSerializer):
    student = serializers.CharField(max_length=255,read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['course_code', 'semister', 'term', 'qtext', 'qimage', 'year', 'student', 'likes']
    
    def get_likes(self, obj):
        return LikeCount.get_likes(obj)
    
    def create(self, validated_data):
        course_code = validated_data.pop('course_code')
        user_id = self.context['user_id']
        (student, created) = Student.objects.get_or_create(user_id=user_id)
        question = Question(**validated_data)
        question.course_code = course_code
        question.student = student
        question.save()
        return question
    
class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['course_code', 'semister', 'term', 'qtext', 'qimage', 'year']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name']


class CommentSerializer(serializers.ModelSerializer):
    student = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)
    likes = serializers.SerializerMethodField()
    class Meta:
        model = QComment
        fields = ['id', 'comment', 'student', 'likes']
    
    def get_likes(self, obj):
        return LikeCount.get_likes(obj)

    def create(self, validated_data):
        user_id = self.context['user_id']
        (student, created) = Student.objects.get_or_create(user_id=user_id)
        return QComment.objects.create(question_id=self.context['question_id'], student = student , **validated_data)


class CComentSerializer(serializers.ModelSerializer):
    student = serializers.CharField(max_length=255,read_only="True")
    comment_id = serializers.IntegerField(read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = CComment
        fields = ["description", "cimage", "comment_id", "student", "likes"]
    
    def get_likes(self, obj):
        return LikeCount.get_likes(obj)

    def create(self, validated_data):
        user_id = self.context['user_id']
        (student, created) = Student.objects.get_or_create(user_id=user_id)
        return CComment.objects.create(
                    comment_id=self.context['comment_id'],
                    student = student,
                    **validated_data
                )



class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'user_id', 'semister']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'content_type', 'object_id']

    def create(self, validated_data):
        ctype = ContentType.objects.get(model=self.context['content_type'])
        like = Like(object_id=self.context['object_id'], student_id = self.context['student_id'])
        like.content_type = ctype
        return like
        
class LikeCount:
    def get_likes(obj):
        model = type(obj).__name__
        ctype = ContentType.objects.get(model=model.lower())
        count = Like.objects.filter(content_type=ctype,object_id=obj.id).count()
        return count