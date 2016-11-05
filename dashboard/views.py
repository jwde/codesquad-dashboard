from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import Student
# Create your views here.
@login_required(login_url='login/')
def index(request):
    return HttpResponse("hello world")
def create_user(request):

    user = User.objects.create(first_name=request.first_name, last_name=request.last_name, email=request.email,
                               username=request.username, password=request.password)
    user.save()
    if request.role == 'student':
        student = Student(user_ptr = user)
        student.save()
        return HttpResponse('<h1>It\'s a Student!</h1>')
    return HttpResponse()
