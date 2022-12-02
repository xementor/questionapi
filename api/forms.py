from django import forms

from api.models import QComment

class QuestionCommentForm(forms.ModelForm):
    comment = forms.CharField(required=True)
    cimage = forms.ImageField(required=False)
    
    class Meta:
        model = QComment
        # fields = ['student','comment','cimage']
        exclude = ('student',)

    