from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
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
    class Meta:
        abstract = True

class Student(Profile):
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
        return self.user.username

class Course(BaseModel):
    name = models.CharField(max_length=200)
    enrolled_users = models.ManyToManyField(User, through='Enrollment')
    def __str__(self):
        return self.name

class Enrollment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField()
