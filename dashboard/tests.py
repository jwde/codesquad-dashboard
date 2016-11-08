from django.test import TestCase
from models import Student, Course, Enrollment, Teacher, Employer

class TeacherTestCase(TestCase):
    def setUp(self):
        teach = Teacher.objects.create(username="teacher01",password="i<3teaching",first_name="Teach",
                               last_name="Er", email="teacher@gmail.com")
        c1 = Course.objects.create(name="Course1")
        teach.course.add(c1)
        teach.save()

    def test_teachers(self):
        teach = Teacher.objects.get(first_name="Teach")
        self.assertEqual(teach.last_name,"Er")

    def test_course_teachers(self):
        teach = Teacher.objects.get(first_name="Teach")
        self.assertEqual(teach.course.get(name="Course1").name,"Course1")

class StudentTestCase(TestCase):
    def setUp(self):
        dboyer = Student.objects.create(username="horsecrzy85",password="i<3horses",first_name="Droolia",
                               last_name="Boyer", email="dboyer@gmail.com")
        html = Course.objects.create(name="Intro to CSS/HTML")
        e1 = Enrollment(student=dboyer,course=html,start_date="2016-10-10")
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
        self.assertEqual(html.enrolled_students.get(pk=dboyer.pk).first_name, "Droolia")

def EmployerTestCase(TestCase):
    def setUp(self):
        empl = Employer.objects.create(username="employer01",password="i<3bosses",first_name="Employ",
                               last_name="Er", email="employer@gmail.com", description="This company makes robots.")
        empl.save()

    def test_employer(self):
        empl = Employer.objects.get(email="employer@gmail.com")
        self.assertEqual(empl.first_name,"Employ")
        self.assertEqual(empl.description, "This company makes robots.")

# example mock / test case
class AlwaysPassThisTest(TestCase):
    def setUp(self):
        # set up mock model
        #(modelname).objects.create(field1="value1", field2="value2")
        pass

    # tests must start with 'test_'
    def test_always_passes(self):
        self.assertEqual(True, True)
