from dataclasses import field, fields
from pickletools import read_long1
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer

from .models import CComment, Course, QComment, Question, Student


class QuestionSerializer(serializers.ModelSerializer):
    student = serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = Question
        fields = ['course_code', 'semister', 'term', 'qtext', 'qimage', 'year', 'student']
    
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
    class Meta:
        model = QComment
        fields = ['id', 'comment', 'student']
    

    def create(self, validated_data):
        user_id = self.context['user_id']
        (student, created) = Student.objects.get_or_create(user_id=user_id)
        return QComment.objects.create(question_id=self.context['question_id'], student = student , **validated_data)


class CComentSerializer(serializers.ModelSerializer):
    student = serializers.CharField(max_length=255,read_only="True")
    comment_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CComment
        fields = ["description", "cimage", "comment_id", "student"]

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