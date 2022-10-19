from dataclasses import field, fields
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer

from .models import CComment, Course, QComment, Question, Student


class QuestionSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = ['course_code', 'semister', 'term', 'qtext', 'qimage', 'year', 'student_id']
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        (student, created) = Student.objects.get_or_create(user_id=user_id)
        question =  Question(student=student, **validated_data)
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
    class Meta:
        model = QComment
        fields = ['comment', 'student']
    

    def create(self, validated_data):
        return QComment.objects.create(question_id=self.context['question_id'], **validated_data)


class CComentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CComment
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'user_id', 'semister']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email']