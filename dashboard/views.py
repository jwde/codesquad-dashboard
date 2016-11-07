from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import Student

# Create your views here.
@login_required(login_url='login/')
def dashboard(request):
    return render(request, "student_dashboard.html", {})

def create_user(request):
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = User.objects.create(first_name=first_name,\
                                       last_name=last_name,\
                                       email=email,\
                                       username=username,\
                                       password=password)
            user.save()
            if request.role == 'student':
                student = Student(user_ptr = user)
                student.save()
                return HttpResponse('<h1>It\'s a Student!</h1>')
    return HttpResponse()
