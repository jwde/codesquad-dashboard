from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import Profile, Student, Teacher, Employer, FormTemplate, Enrollment, Question, FormResponse, QuestionResponse
from forms import RegisterForm, DynamicForm
from utils import order

# Create your views here.
@login_required(login_url='login/')
def dashboard(request):
    if request.method == 'GET':
        return render(request, "student_dashboard.html", 
                      {'name': request.user.first_name + " " + 
                               request.user.last_name})

@login_required(login_url='login/')
def form(request, form_id):
    def form_allowed(user, form):
        student_in_class = user.profile.is_student and\
                           Enrollment.objects.filter(student=user.profile.student,\
                                                     course=form.course).exists()
        global_allowed = (user.profile.is_student and form.students_allowed) or\
                         (user.profile.is_teacher and form.teachers_allowed) or\
                         (user.profile.is_employer and form.employers_allowed)
        return student_in_class or global_allowed

    form_query = FormTemplate.objects.filter(pk=form_id)
    form_m = form_query[0] if form_query.count() == 1 else None
    if (request.method == 'GET' or request.method == 'POST') and\
       form_m and form_allowed(request.user, form_m):
        question_ids = [int(q) for q in form_m.question_list.split(',')]
        questions = Question.objects.filter(id__in=question_ids)\
                    .extra(select={'o': order('id', question_ids)}, order_by=('o',))
        named_questions = enumerate(questions)
        form = DynamicForm(request.POST or None, fields=named_questions)
        if request.method == 'POST':
            if form.is_valid():
                form_response = FormResponse.objects.create(form_template=form_m,\
                                                            user=request.user)
                question_responses = [QuestionResponse.objects.create(user=request.user,\
                                                                      question=questions[n],\
                                                                      response_text=v)\
                                      for n,v in [(int(n),v) for n,v in form.custom_responses()]]
                for r in question_responses:
                    r.save()
                form_response.save()
            return redirect('dashboard')
        return render(request, 'form.html', {'form': form, 'form_id': form_id})
    else:
        return redirect('dashboard')

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
