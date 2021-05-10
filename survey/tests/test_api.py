import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from ..models import Survey
from django.test import TestCase



class SurveyListApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_survey(self):
        """
        Ensure we can create a new survey object
        """
        url = reverse('survey-list')
        data = {
                "name": "Test2",
                "description": "2nd Survey Test",
                "category": 1,
                "pub_date": "2021-05-13T17:58:24Z",
                "exp_date": "2021-05-16T17:58:24Z"
            }
        response = self.client.post(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 1)
        self.assertEqual(Survey.objects.get().name, 'Test2')