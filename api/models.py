from email.policy import default
from pydoc import describe
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Student(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=55)
    semister = models.IntegerField()

    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=55, primary_key=True)
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

class Question(models.Model):
    semister = models.IntegerField()
    term = models.CharField(max_length=10)
    year = models.IntegerField()
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    qimage = models.ImageField(upload_to="questions")
    qtext = models.CharField(max_length=255,null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, default=203153927)

    def __str__(self):
        return f'{str(self.course_code)} {self.semister}  {self. year}'

class QComment(models.Model):
    comment = models.CharField(max_length=255)
    cimage = models.ImageField(null=True,blank=True,upload_to="comments")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

class CComment(models.Model):
    description = models.CharField(max_length=255, default="")
    cimage = models.ImageField(null=True,blank=True,upload_to="comments")
    comment = models.ForeignKey(QComment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

class Like(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    
    def __str__(self):
        return self.content_type





