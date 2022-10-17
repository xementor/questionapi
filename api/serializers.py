from dataclasses import field, fields
from rest_framework import serializers

from .models import CComment, Course, QComment, Question


class QuestionSerializer(serializers.ModelSerializer):
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