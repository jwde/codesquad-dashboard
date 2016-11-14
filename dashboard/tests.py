from django.test import TestCase
from models import Student, Course, Enrollment
from django.test import Client
from django.contrib.auth.models import User


class StudentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='horsecrzy85',\
                                        password='i<3horses',\
                                        first_name='Droolia',\
                                        last_name='Boyer',\
                                        email='dboyer@gmail.com')
        user.save()
        dboyer = Student.objects.create(user=user,\
                                        privacy_setting='PR')
        dboyer.save()
        html = Course.objects.create(name="Intro to CSS/HTML")
        html.save()
        e1 = Enrollment(user=dboyer.user,course=html,start_date="2016-10-10")
        e1.save()

    def test_students(self):
        """ Just tests if it was created in the database, the default is private, and can be updated """
        droolia = User.objects.get(first_name='Droolia').profile
        self.assertEqual(droolia.user.first_name,"Droolia")
        self.assertEqual(droolia.privacy_setting, "PR")
        droolia.privacy_setting = "PU"
        droolia.save()
        self.assertEqual(droolia.privacy_setting, "PU")

    def test_enrollment(self):
        html = Course.objects.get(name="Intro to CSS/HTML")
        dboyer = User.objects.get(first_name="Droolia").profile
        self.assertEqual(html.enrolled_users.get(pk=dboyer.pk).first_name, "Droolia")

class CreateUserTestCase(TestCase):
    def setUp(self):
        client = Client()

    def test_create_user(self):

        response = self.client.post('/register/', {'username': 'craycray',\
                                                   'password1': 'ialso<3horses',\
                                                   'password2': 'ialso<3horses',\
                                                   'first_name': 'Max',\
                                                   'last_name' : 'Boyer',\
                                                   'email': 'whodat@idk.com',\
                                                   'role': 'student'})
        student = User.objects.get(username='craycray').profile
        self.assertEqual(student.user.first_name, 'Max')


# example mock / test case
class AlwaysPassThisTest(TestCase):
    def setUp(self):
        # set up mock model
        #(modelname).objects.create(field1="value1", field2="value2")
        pass

    # tests must start with 'test_'
    def test_always_passes(self):
        self.assertEqual(True, True)
