from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
import datetime

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,\
                                      blank=True,\
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,\
                                      blank=True,\
                                      null=True)
    class Meta:
        abstract = True

class Profile(BaseModel):
    user = models.OneToOneField(User,\
                                on_delete=models.CASCADE,\
                                primary_key=True,\
                                related_name='profile')
    _is_student = models.BooleanField(default=True)
    _is_teacher = models.BooleanField(default=False)
    teacher_approved = models.BooleanField(default=False)
    _is_employer = models.BooleanField(default=False)
    employer_approved = models.BooleanField(default=False)

    @property
    def is_student(self):
        return self._is_student
    @property
    def is_teacher(self):
        return self._is_teacher and self.teacher_approved
    @property
    def is_employer(self):
        return self._is_employer and self.employer_approved
    @property
    def type(self):
        if self.is_employer:
            return 'employer'
        elif self.is_teacher:
            return 'teacher'
        elif self.is_student:
            return 'student'
        else:
            return 'pending'
    def __str__(self):
        return self.user.__str__()

class Student(BaseModel):
    profile = models.OneToOneField(Profile,\
                                   on_delete=models.CASCADE,\
                                   primary_key=True,\
                                   related_name='student')
    PRIVATE = 'PR'
    PUBLIC = 'PU'
    PRIVACY_CHOICES = (
    	('PR', 'Private'),
    	('PU', 'Public'),
    )
    privacy_setting = models.CharField(
    	max_length=2,
    	choices=PRIVACY_CHOICES,
        default=PRIVATE,
    )
    def __str__(self):
        return self.profile.user.username

class Course(BaseModel):
    name = models.CharField(max_length=200)
    enrolled_students = models.ManyToManyField(Student, through='Enrollment')
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.name

class Enrollment(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Teacher(BaseModel):
    profile = models.OneToOneField(Profile,\
                                   on_delete=models.CASCADE,\
                                   primary_key=True,\
                                   related_name='teacher')
    courses = models.ManyToManyField(Course)
    def __str__(self):
        return self.profile.user.username

class Employer(BaseModel):
    profile = models.OneToOneField(Profile,\
                                   on_delete=models.CASCADE,\
                                   primary_key=True,\
                                   related_name='employer')
    description = models.TextField()
    def __str__(self):
        return self.profile.user.username

class FormTemplate(models.Model):
    question_list = models.TextField(validators=[validators.validate_comma_separated_integer_list])
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Question(models.Model):

    LONGFORM = 'LF'
    SHORTFORM = 'SF'
    MULTIPLE_CHOICE = 'MC'
    SLIDING_SCALE = 'SS'
    QUESTION_TYPES = (
        ('LF', 'Long Form Text'),
        ('SF', 'Short Form Text'),
        ('MC', 'Multiple Choice'),
        ('SS', 'Sliding Scale'),
    )
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default=LONGFORM,
    )
    additional_info = JSONField()
    question_text = models.TextField()
    question_number = models.IntegerField(default=1)

class FormResponse(models.Model):
    form_template = models.ForeignKey(FormTemplate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class QuestionResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_text = models.TextField()
