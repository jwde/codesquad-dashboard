from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from models import Profile, Student, Teacher, Employer, FormTemplate, Enrollment, Question, FormResponse, QuestionResponse, Course
from forms import RegisterForm, DynamicForm, EditProfileForm
from utils import order
from collections import defaultdict
import datetime
import json
import bleach

# Create your views here.
@login_required(login_url='/login/')
def dashboard(request, type_requested=None):
    def validate(type_requested):
        return type_requested in ('student', 'teacher', 'employer') and\
               {'student': lambda: request.user.profile.is_student,\
                'teacher': lambda: request.user.profile.is_teacher,\
                'employer': lambda: request.user.profile.is_employer}[type_requested]()
    def student_dashboard():
        return render(request, "student_dashboard.html", 
                      {'name': request.user.first_name + " " + 
                               request.user.last_name,\
                       'about': request.user.profile.student.about_me,\
                       'projects': request.user.profile.student.projects})
    def teacher_dashboard():
        active_courses = [c for c in request.user.profile.teacher.courses\
                          if c.end_date >= datetime.date.today()]
        student_sets = [frozenset(c.enrolled_students.all()) for c in active_courses.all()]
        students = frozenset().union(*student_sets)
        student_names = ['{} {}'.format(s.profile.user.first_name, s.profile.user.last_name)\
                         for s in students]
        return render(request, "teacher_dashboard.html",\
                      {'students': student_names})
    def employer_dashboard():
        active_courses = Course.objects.filter(end_date__gte = datetime.date.today())
        student_sets = [frozenset(c.enrolled_students.filter(privacy_setting='PU'))\
                        for c in active_courses.all()]
        students = frozenset().union(*student_sets)
        student_profiles = []
        for s in students:
            name = '{} {}'.format(s.profile.user.first_name, s.profile.user.last_name)
            profile = {'name': name, 'about': s.about_me, 'projects': s.projects,}
            student_profiles.append(profile)
        return render(request, "employer_dashboard.html",\
                      {'students': student_profiles})
    def pending_dashboard():
        return render(request, "pending_dashboard.html")
    type_returned = type_requested if validate(type_requested)\
                    else request.user.profile.type
    if request.method == 'GET':
        return\
        {'student': student_dashboard,\
         'teacher': teacher_dashboard,\
         'employer': employer_dashboard,\
         'pending': pending_dashboard}[type_returned]()

@login_required(login_url='/login/')
def edit_profile(request):
    if request.user.profile.is_student:
        form = EditProfileForm(request.POST or None, student=request.user.profile.student)
        if request.method == 'POST':
            if form.is_valid():
                request.user.profile.student.about_me = form.cleaned_data['about_me']
                request.user.profile.student.projects = form.cleaned_data['projects']
                request.user.profile.student.save()
                return redirect('dashboard')
        return render(request, 'edit_profile.html', {'form': form})
    return redirect('dashboard')

@login_required(login_url='/login/')
def my_forms(request):
    created_forms = FormTemplate.objects.filter(owner=request.user)
    viewable_forms_sets = []
    if request.user.profile.is_student:
        viewable_forms_sets.append(frozenset(FormTemplate.objects.filter(students_allowed=True)))
    if request.user.profile.is_teacher:
        viewable_forms_sets.append(frozenset(FormTemplate.objects.filter(teachers_allowed=True)))
    if request.user.profile.is_employer:
        viewable_forms_sets.append(frozenset(FormTemplate.objects.filter(employers_allowed=True)))
    viewable_forms = frozenset().union(*viewable_forms_sets)
    return render(request, 'my_forms.html',\
                  {'view_forms': viewable_forms,\
                   'own_forms': created_forms})

@login_required(login_url='/login/')
def form_responses(request, form_id):
    form_query = FormTemplate.objects.filter(pk=form_id)
    if form_query.exists():
        form = form_query[0]
        if form.owner == request.user:
            questions = [int(q) for q in form.question_list.split(',')]
            questions_data = [{'id': q, 'text': Question.objects.get(pk=q).question_text} for q in questions]
            question_responses = QuestionResponse.objects.filter(question__in=questions)
            response_by_user = defaultdict(dict)
            for qr in question_responses:
                response_by_user[qr.user.pk][qr.question.pk] = qr.response_text
            for u in response_by_user:
                response_by_user[u] = [(q['text'], response_by_user[u][q['id']]) for q in questions_data]
            user_ids = question_responses.values('user').distinct()
            users = User.objects.filter(pk__in=user_ids)
            user_data = [{'name': u.first_name + ' ' + u.last_name,\
                          'id': u.pk} for u in users]
            responses = [(user_data, response_by_user[u['id']]) for u in user_data]
            return render(request, 'form_responses.html',\
                          {'name': form.name, 'responses': responses})
    return redirect('dashboard')


@login_required(login_url='/login/')
def form(request, form_id):
    def form_allowed(user, form):
        student_in_class = user.profile.is_student and\
                           Enrollment.objects.filter(student=user.profile.student,\
                                                     course=form.course).exists()
        global_allowed = (user.profile.is_student and form.students_allowed) or\
                         (user.profile.is_teacher and form.teachers_allowed) or\
                         (user.profile.is_employer and form.employers_allowed)
        is_owner = form.owner == user
        return student_in_class or global_allowed or is_owner

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
            profile = Profile.objects.create(user=user,\
                                             _is_student=(role == 'student'),\
                                             _is_teacher=(role == 'teacher'),\
                                             _is_employer=(role == 'employer'),\
                                             )
            user.save()
            profile.save()
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

@login_required(login_url='login/')
def create_form(request):
    if request.method == 'POST':# and request.user.profile.is_teacher:
        try:
            form_json = json.loads(request.POST.get('form'))
            name = bleach.clean(form_json['name'])
            questions = []
            for question in form_json['questions']:
                question_type = question['question_type']
                question_text = bleach.clean(question['question_text'])
                additional_info = question['additional_info']
                if not question_type in frozenset(('LF', 'SF', 'MC', 'SS', 'SM')):
                    return HttpResponseForbidden()
                if 'choices' in additional_info:
                    additional_info['choices'] = bleach.clean(additional_info['choices'])
                if 'range_max' in additional_info:
                    additional_info['range_max'] = int(additional_info['range_max'])
                if 'range_min' in additional_info:
                    additional_info['range_min'] = int(additional_info['range_min'])
                additional_info = {k: additional_info[k]\
                                   for k in ['choices', 'range_max', 'range_min']\
                                   if k in additional_info}
                question_model = Question.objects.create(question_type=question_type,\
                                                         question_text=question_text,\
                                                         additional_info=additional_info)
                question_model.save()
                questions.append(str(question_model.pk))
            # right now we have no idea what course this is for -- must add that
            form_template = FormTemplate.objects.create(question_list=','.join(questions),\
                                                        owner=request.user,\
                                                        name=name)
            form_template.save()
        except:
            return HttpResponseForbidden()
    return render(request, "editforms.html", {});

def template_short_answer(request):
    if request.method == 'GET':
        return render(request, "question_templates/short_answer.html", {});

def template_long_answer(request):
    if request.method == 'GET':
        return render(request, "question_templates/long_answer.html", {});

def template_multiple_choice(request):
    if request.method == 'GET':
        return render(request, "question_templates/multiple_choice.html", {});

def template_slider(request):
    if request.method == 'GET':
        return render(request, "question_templates/slider.html", {});

def template_invalid_form(request):
    if request.method == 'GET':
        return render(request, "question_templates/invalid_form.html", {});
