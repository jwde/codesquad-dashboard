from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import Profile, Student, Teacher, Employer
from forms import RegisterForm

# Create your views here.
@login_required(login_url='login/')
def dashboard(request):
    return render(request, "student_dashboard.html", {})
def view_user(request):
    return render(request, "temp_user.html", {})
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password1')
            role = request.POST.get('role')
            user = User.objects.create_user(
                                       username,\
                                       email,\
                                       password,\
                                       last_name=last_name,\
                                       first_name=first_name)
            user.save()
            profile = Profile.objects.create(user=user,\
                                             _is_student=(role == 'student'),\
                                             _is_teacher=(role == 'teacher'),\
                                             _is_employer=(role == 'employer'),\
                                             )
            if role == 'teacher':
                teacher = Teacher(profile = profile)
                teacher.save()
            elif role == 'employer':
                employer = Employer(profile = profile)
                employer.save()
            else:
                student = Student(profile = profile,\
                                  privacy_setting = 'PR')
                student.save()
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    return render(request, 'createaccount.html', {'form': form})
