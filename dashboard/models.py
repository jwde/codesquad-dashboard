from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


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
	created_at = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_at = datetime.datetime.today()
		return super(Student,self).save(*args, **kwargs)

	def __str__(self):
		return self.username

class Course(models.Model):
	name = models.CharField(max_length=200)
	enrolled_users = models.ManyToManyField(User, through='Enrollment')
	created_at = models.DateTimeField(editable=False,default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_at = datetime.datetime.today()
		self.last_modified = datetime.datetime.today()
		return super(Course,self).save(*args, **kwargs)


	def __str__(self):
		return self.name

class Enrollment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	start_date = models.DateField()
	created_at = models.DateTimeField(editable=False,default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_at = datetime.datetime.today()
		self.last_modified = datetime.datetime.today()
		return super(Enrollment,self).save(*args, **kwargs)
