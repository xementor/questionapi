from dataclasses import field
from django import forms
from requests import Response

from api.models import QComment

class QuestionCommentForm(forms.ModelForm):
    class Meta:
        model = QComment
        fields = ['student','comment','cimage']

    