from django.contrib import admin
from .models import Course, Student, Question, QComment, CComment, Like

# Register your models here.admin.site.register(Vote)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Course)
admin.site.register(QComment)
admin.site.register(CComment)
admin.site.register(Like)
