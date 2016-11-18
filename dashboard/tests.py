from django.test import TestCase
from models import Profile, Student, Teacher, Employer, Course, Enrollment
from django.test import Client
from django.contrib.auth.models import User
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
