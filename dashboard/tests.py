from django.test import TestCase
from models import Student


class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(username="horsecrzy85",password="i<3horses",first_name="Droolia",
                               last_name="Boyer", email="dboyer@gmail.com",course="Basics of HTML/CSS")

    def test_students(self):
        """ Just tests if it was created in the database, the default is private, and can be updated """
        droolia = Student.objects.get(first_name="Droolia")
        self.assertEqual(droolia.first_name,"Droolia")
        self.assertEqual(droolia.privacy_setting, "PR")
        droolia.privacy_setting = "PU"
        droolia.save()
        self.assertEqual(droolia.privacy_setting, "PU")

# example mock / test case
class AlwaysPassThisTest(TestCase):
    def setUp(self):
        # set up mock model
        #(modelname).objects.create(field1="value1", field2="value2")
        pass

    # tests must start with 'test_'
    def test_always_passes(self):
        self.assertEqual(True, True)
