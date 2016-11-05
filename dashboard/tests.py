from django.test import TestCase
from models import Student, Course, Enrollment
from django.test import Client


class StudentTestCase(TestCase):
    def setUp(self):
        dboyer = Student.objects.create(username="horsecrzy85",password="i<3horses",first_name="Droolia",
                               last_name="Boyer", email="dboyer@gmail.com")
        html = Course.objects.create(name="Intro to CSS/HTML")
        e1 = Enrollment(user=dboyer,course=html,start_date="2016-10-10")
        e1.save()

    def test_students(self):
        """ Just tests if it was created in the database, the default is private, and can be updated """
        droolia = Student.objects.get(first_name="Droolia")
        self.assertEqual(droolia.first_name,"Droolia")
        self.assertEqual(droolia.privacy_setting, "PR")
        droolia.privacy_setting = "PU"
        droolia.save()
        self.assertEqual(droolia.privacy_setting, "PU")

    def test_enrollment(self):
        html = Course.objects.get(name="Intro to CSS/HTML")
        dboyer = Student.objects.get(first_name="Droolia")
        self.assertEqual(html.enrolled_users.get(pk=dboyer.pk).first_name, "Droolia")

class CreateUserTestCase(TestCase):
    def setUp(self):
        client = Client()

    def test_create_user(self):

        response = self.client.get('/create_user/', {'username': 'craycray', 'password': 'ialso<3horses', 'firstname': 'Max',
                                        'lastname' : 'Boyer', 'email': 'whodat@idk.com','role': 'student'})
        self.assertEqual(response, '<h1>It\'s a Student!</h1>')


# example mock / test case
class AlwaysPassThisTest(TestCase):
    def setUp(self):
        # set up mock model
        #(modelname).objects.create(field1="value1", field2="value2")
        pass

    # tests must start with 'test_'
    def test_always_passes(self):
        self.assertEqual(True, True)
