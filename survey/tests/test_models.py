from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from ..models import Survey, Category
from django.contrib.auth.models import User


class SurveyTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create()
        self.category = Category.objects.create(name="I am a test Category")
        self.name = 'Test Survey'
        self.description = 'This is just a test Survey'
        self.survey = Survey(
            name=self.name,
            description=self.description,
            category=self.category
        )

    def test_survey_was_created(self):
        number_of_objs_before = Survey.objects.count()
        self.survey.save()
        number_of_objs_after = Survey.objects.count()
        self.assertNotEqual(number_of_objs_before, number_of_objs_after)
        self.assertEqual(number_of_objs_before + 1, number_of_objs_after)
        self.assertEqual(self.survey.name, self.name)

    def test_survey__str__(self):
        self.assertEqual(self.survey.__str__(), f'{self.name}: {self.description}')

    def test_add_users_to_survey(self):
        self.survey.save()
        self.survey.users.add(self.user1)
        self.assertEqual(self.survey.users.all()[0], self.user1)
        


