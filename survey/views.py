from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.reverse import reverse
from django.contrib.auth.models import User, Group
from django.http import Http404
from django.core.exceptions import ValidationError

from .models import Survey, Category, Question, Answer
from survey.serializers import SurveySerializer, CategorySerializer, PostSurveySerializer, PostAddQuestionSerializer, QuestionSerializer, AnswerSerializer

# Create your views here.


class CategoryList(APIView):

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)




class SurveyList(APIView):
    """
    API endpoint that returns all the surveys,
    creates a new survey with some questions
    updates and delete survey
    """

    def get(self, request, format=None):
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create new Survey and add some Questions
        """
        serializer = PostSurveySerializer(data=request.data)
        if serializer.is_valid():
            try:
                category = Category.objects.get(pk=request.data.get('category'))
            except:
                raise Http404

            survey = Survey(
                name=request.data['name'],
                description=request.data.get('description'),
                category=category,
                pub_date=request.data.get('pub_date'),
                exp_date=request.data.get('exp_date'),
                period=request.data.get('period')
            )

            survey.save()

            if request.data.get("user_emails"):
                users = User.objects.filter(email__in=request.data.get('user_emails'))
                survey.users.add(*users)
            if request.data.get("groups"):
                groups = Group.objects.filter(id__in=request.data.get('groups'))
                survey.groups.add(*groups)

            if request.data.get('questions'):
                question_list = [Question(**dict(item, survey=survey)) for item in request.data['questions']]
                Question.objects.bulk_create(question_list)


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SurveyDetail(APIView):
    """
    Retrieve, update or delete a Survey
    Also retrieve questions of a survey
    """
    def get_object(self, pk):
        try:
            return Survey.objects.get(pk=pk)
        except Survey.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        from django.urls import reverse
        survey = self.get_object(pk)
        if request.get_full_path() == reverse('survey_questions', args=[pk]):
            serializer = QuestionSerializer(survey.get_questions, many=True)
        else:
            serializer = SurveySerializer(survey)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = PostAddQuestionSerializer(data=request.data)
        if serializer.is_valid():
            survey = self.get_object(pk)

            if request.data.get('questions'):
                question_list = [Question(**dict(item, survey=survey)) for item in request.data['questions']]
                Question.objects.bulk_create(question_list)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        survey = self.get_object(pk)
        serializer = SurveySerializer(survey, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        survey = self.get_object(pk)
        survey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionDetail(APIView):

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Survey.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk, format=None):

        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            question =  self.get_object(pk)
            try:
                user = User.objects.get(email=request.data.get('user_email'))
            except User.DoesNotExist:
                raise Http404

            Answer.objects.create(
                text=self.request.data.get('answer'),
                question=question,
                user=user
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











