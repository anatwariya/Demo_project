from django.test import TestCase
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectApp0.settings")


class YourTestClass(TestCase):
    def setUp(self):
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)
