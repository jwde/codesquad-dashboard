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
	course = models.CharField(max_length=200)



