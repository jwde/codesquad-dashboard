from django.test import TestCase
from models import Profile, Student, Teacher, Employer, Course, Enrollment, FormTemplate, Question, FormResponse, QuestionResponse
from django.test import Client
from django.contrib.auth.models import User
from utils import order
import datetime


class StudentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='horsecrzy85',\
                                        password='i<3horses',\
                                        first_name='Droolia',\
                                        last_name='Boyer',\
                                        email='dboyer@gmail.com')
        user.save()
        profile = Profile.objects.create(user=user,\
                                         _is_student=True,\
                                         _is_teacher=False,\
                                         _is_employer=False)
        dboyer = Student.objects.create(profile=profile,\
                                        privacy_setting='PR')
        dboyer.save()
        html = Course.objects.create(name="Intro to CSS/HTML",
                                     start_date=datetime.date(2016, 10, 10),\
                                     end_date=datetime.date(2016, 11, 10)\
                )
        html.save()
        e1 = Enrollment(student=dboyer,\
                        course=html,\
                        )
        e1.save()

    def test_students(self):
        """ Just tests if it was created in the database, the default is private, and can be updated """
        droolia = User.objects.get(first_name='Droolia').profile.student
        self.assertEqual(droolia.profile.user.first_name,"Droolia")
        self.assertEqual(droolia.privacy_setting, "PR")
        droolia.privacy_setting = "PU"
        droolia.save()
        self.assertEqual(droolia.privacy_setting, "PU")

    def test_enrollment(self):
        html = Course.objects.get(name="Intro to CSS/HTML")
        dboyer = User.objects.get(first_name="Droolia").profile.student
        self.assertEqual(html.enrolled_students.get(pk=dboyer.pk).profile.user.first_name, "Droolia")

class CreateUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        self.client.post('/register/', {'username': 'craycray',\
                                                    'password1': 'ialso<3horses',\
                                                    'password2': 'ialso<3horses',\
                                                    'first_name': 'Max',\
                                                    'last_name' : 'Boyer',\
                                                    'email': 'whodat@idk.com',\
                                                    'role': 'student'})
        student = User.objects.get(username='craycray').profile.student
        self.assertEqual(student.profile.user.first_name, 'Max')

class QuestionTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='horsecrzy85',\
                                        password='i<3horses',\
                                        first_name='Droolia',\
                                        last_name='Boyer',\
                                        email='dboyer@gmail.com')
        user.save()

        question = Question.objects.create(question_type='MC',\
                                           question_text='Why do you want to join CodeSquad?',\
                                           additional_info='{}')
        question.save()

        response = QuestionResponse.objects.create(user=user,\
                                                   question=question,\
                                                   response_text='bc codesquad is so dope, man')
        response.save()

    def test_question(self):
        type_of_q = Question.objects.get(question_text='Why do you want to join CodeSquad?').question_type
        self.assertEqual(type_of_q,'MC')

    def test_question_response(self):
        q1 = Question.objects.get(question_text='Why do you want to join CodeSquad?')
        response = QuestionResponse.objects.get(question=q1)
        self.assertEqual(response.user.first_name, 'Droolia')

class FormTemplateTestCase(TestCase):
    def setUp(self):
        question1 = Question.objects.create(question_type='MC',\
                                           question_text='Why do you want to join CodeSquad?',\
                                           additional_info='{}')
        question2 = Question.objects.create(question_type='LT',\
                                           question_text='What is your favorite hobby?',\
                                           additional_info='{}')
        question1.save()
        question2.save()

        user = User.objects.create_user(username='horsecrzy85',\
                                        password='i<3horses',\
                                        first_name='Droolia',\
                                        last_name='Boyer',\
                                        email='dboyer@gmail.com')
        user.save()

        template = FormTemplate.objects.create(name='Quiz1',\
                                               owner=user,\
                                               question_list='{},{}'\
                                               .format(question1.id, question2.id))
        template.save()

    def test_form_template(self):
        question_ids = FormTemplate.objects.get(name='Quiz1').question_list.split(',')
        questions = [Question.objects.get(id=int(q)) for q in question_ids]
        self.assertEqual(questions[0].question_type, 'MC')
        self.assertEqual(questions[1].question_text, 'What is your favorite hobby?')

class FormResponseTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='horsecrzy85',\
                                        password='i<3horses',\
                                        first_name='Droolia',\
                                        last_name='Boyer',\
                                        email='dboyer@gmail.com')
        user.save()

        template = FormTemplate.objects.create(name='Quiz1',\
                                               owner=user,\
                                               question_list='1,4,5')
        template.save()

        profile = Profile.objects.create(user=user,\
                                         _is_student=True,\
                                         _is_teacher=False,\
                                         _is_employer=False)

        dboyer = Student.objects.create(profile=profile,\
                                        privacy_setting='PR')
        dboyer.save()

        form_response = FormResponse.objects.create(user=user,\
                                                    form_template=template)
        form_response.save()

    def test_form_response(self):
        user = User.objects.get(first_name='Droolia')
        response = FormResponse.objects.get(user=user)

        self.assertEqual(response.form_template.name,'Quiz1')
        self.assertEqual(user.formresponse_set.count(), 1)

class QuestionResponseTestCase(TestCase):
    def setUp(self):
        question1 = Question.objects.create(question_type='MC',\
                                           question_text='Why do you want to join CodeSquad?',\
                                           additional_info='{}')
        question2 = Question.objects.create(question_type='LT',\
                                           question_text='What is your favorite hobby?',\
                                           additional_info='{}')
        question1.save()
        question2.save()
        user = User.objects.create_user(username='horsecrzy85',\
                                        password='i<3horses',\
                                        first_name='Droolia',\
                                        last_name='Boyer',\
                                        email='dboyer@gmail.com')
        user.save()
        template = FormTemplate.objects.create(name='Quiz1',\
                                               owner=user,\
                                               question_list='{},{}'\
                                               .format(question1.id, question2.id))
        template.save()
        profile = Profile.objects.create(user=user,\
                                         _is_student=True,\
                                         _is_teacher=False,\
                                         _is_employer=False)

        dboyer = Student.objects.create(profile=profile,\
                                        privacy_setting='PR')
        dboyer.save()
        form_response = FormResponse.objects.create(user=user,\
                                                    form_template=template)
        q1_response = QuestionResponse.objects.create(user=user,\
                                                      question=question1,\
                                                      response_text='codesquad is so cool')
        q2_response = QuestionResponse.objects.create(user=user,\
                                                      question=question2,\
                                                      response_text='codesquadding')
        form_response.save()
        q1_response.save()
        q2_response.save()
        user2 = User.objects.create_user(username='horsecrzy86',\
                                        password='i<3horsesaswell',\
                                        first_name='Droolia',\
                                        last_name='Boyer',\
                                        email='dboyer2@gmail.com')
        user2.save()
        profile2 = Profile.objects.create(user=user2,\
                                         _is_student=True,\
                                         _is_teacher=False,\
                                         _is_employer=False)

        dboyer2 = Student.objects.create(profile=profile2,\
                                        privacy_setting='PR')
        dboyer2.save()
        form_response2 = FormResponse.objects.create(user=user2,\
                                                    form_template=template)
        q1_response2 = QuestionResponse.objects.create(user=user2,\
                                                      question=question1,\
                                                      response_text='codesquad is dope')
        q2_response2 = QuestionResponse.objects.create(user=user2,\
                                                      question=question2,\
                                                      response_text='codesquadding')

        form_response2.save()
        q1_response2.save()
        q2_response2.save()

    def test_get_question_response(self):
        form = FormTemplate.objects.get(name='Quiz1')
        question_ids = [int(q) for q in form.question_list.split(',')]
        user = User.objects.get(username='horsecrzy85')
        responses = QuestionResponse.objects.filter(user=user, question__in=question_ids)\
                    .extra(select={'o': order('question_id', question_ids)}, order_by=('o',))
        self.assertEqual(responses[0].response_text, 'codesquad is so cool')
        self.assertEqual(len(responses), 2)
        

class PromoteUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/register/', {'username': 'craycray',\
                                                    'password1': 'ialso<3horses',\
                                                    'password2': 'ialso<3horses',\
                                                    'first_name': 'Max',\
                                                    'last_name' : 'Boyer',\
                                                    'email': 'whodat@idk.com',\
                                                    'role': 'teacher'})

    def test_approve_teacher(self):
        profile = User.objects.get(username='craycray').profile
        self.assertEqual(profile.type, 'pending')
        profile.teacher_approved = True
        profile.save()
        self.assertEqual(profile.type, 'teacher')
        profile.teacher_approved = False
        profile.save()

    def test_change_to_employer(self):
        profile = User.objects.get(username='craycray').profile
        profile.teacher_approved = True
        employer = Employer.objects.create(profile = profile, description = "BodyBuddy inc.")
        employer.save()
        profile._is_employer = True
        profile.save()
        self.assertEqual(profile.type, 'teacher')
        profile.employer_approved = True
        profile.save()
        self.assertEqual(profile.type, 'employer')

# example mock / test case
class AlwaysPassThisTest(TestCase):
    def setUp(self):
        # set up mock model
        #(modelname).objects.create(field1="value1", field2="value2")
        pass

    # tests must start with 'test_'
    def test_always_passes(self):
        self.assertEqual(True, True)
