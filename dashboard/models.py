from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Student(User):
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
		return self.username

class Course(models.Model):
	name = models.CharField(max_length=200)
	enrolled_students = models.ManyToManyField(Student, through='Enrollment')

	def __str__(self):
		return self.name

class Enrollment(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	start_date = models.DateField()

