from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.reverse import reverse
from django.contrib.auth.models import User, Group
from django.http import Http404
from django.core.exceptions import ValidationError

from .models import Survey, Category, Question, Answer
from survey.serializers import SurveySerializer, CategorySerializer, PostSurveySerializer, \
    PostAddQuestionSerializer, QuestionSerializer, AnswerSerializer

# Create your views here.


class CategoryList(APIView):
    """
    API endpoint that returns all categories, creates a new category
    and updates a new one
    """
    def get(self, request, format=None):
        """
        Returns all categories

        @param request: api request
        @type request: object
        @param format: rendered and media type to use in the response
        @type format: string
        @return: List of Categories objects
        @rtype: Could be json or template based on where the request
        is coming from.If from Browser returns template
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self):
        raise NotImplementedError

    def put(self, request, pk, format=None):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError




class SurveyList(APIView):
    """
    API endpoint that returns all the surveys,
    creates a new survey with some questions
    updates and delete survey
    """

    def get(self, request, format=None):
        """
        Returns list of available Surveys

        @param request: the api request
        @type request:  request object
        @param format:  rendered and media type to use in the response
        @type format:  string
        @return: List of Surveys objects
        @rtype:  REST Response object.
        Could be json or template based on the request
        """
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create new Survey and add some Questions

        @param request:  the api request
        @type request:  request object
        @param format: rendered and media type to use in the response
        @type format: string
        @return: Survey Created
        @rtype:  REST Response object.
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
        """
        Helper function to get a Survey object based on the
        unique identifier passed in pk

        @param pk: object unique identifier (primary key)
        @type pk: int
        @return: Survey object if found else 404 error not found
        @rtype: Survey obj
        """
        try:
            return Survey.objects.get(pk=pk)
        except Survey.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Returns a specific survey if url path is "/surveys/<survey_id>"
        If the path is "/surveys/<survey_id>/questions/" returns list of Questions
        for the specific Survey

        @param request: request object
        @type request: object
        @param pk: Survey unique identifier
        @type pk: int
        @param format:
        @type format:
        @return: Specific survey or List of Questions. Depends on the path
        @rtype: object
        """
        from django.urls import reverse
        survey = self.get_object(pk)
        if request.get_full_path() == reverse('survey_questions', args=[pk]):
            serializer = QuestionSerializer(survey.get_questions, many=True)
        else:
            serializer = SurveySerializer(survey)
        return Response(serializer.data)

    def post(self, request, pk):
        """
        Add Questions to an existing Survey

        @param request: API request
        @type request: object
        @param pk: unique survey identifier or primary key
        @type pk: integer
        @return: Updated Survey
        @rtype: Survey object
        """
        serializer = PostAddQuestionSerializer(data=request.data)
        if serializer.is_valid():
            survey = self.get_object(pk)

            if request.data.get('questions'):
                question_list = [Question(**dict(item, survey=survey)) for item in request.data['questions']]
                Question.objects.bulk_create(question_list)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """
        Updates a Survey.
        All Survey model fields must be provided

        @param request: API request
        @type request: object
        @param pk: Survey unique identifier/ primary key
        @type pk: int
        @param format:
        @type format:
        @return: Updated Survey
        @rtype: Survey json object or template
        """
        survey = self.get_object(pk)
        serializer = SurveySerializer(survey, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Deletes a Survey

        @param request: API Request
        @type request: reqyest object
        @param pk: Survey unique identifier
        @type pk: int
        @param format:
        @type format:
        @return:
        @rtype:
        """
        survey = self.get_object(pk)
        survey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionDetail(APIView):

    def get_object(self, pk):
        """
        Helper funtion to Return Question Object if exists

        @param pk:
        @type pk:
        @return:
        @rtype:
        """
        try:
            return Question.objects.get(pk=pk)
        except Survey.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Returns a Specific Question

        @param request:
        @type request:
        @param pk:
        @type pk:
        @param format:
        @type format:
        @return:
        @rtype:
        """
        question = self.get_object(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        """
        Updates a Question

        @param request:
        @type request:
        @param pk:
        @type pk:
        @param format:
        @type format:
        @return:
        @rtype:
        """
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Deletes a Question

        @param request:
        @type request:
        @param pk:
        @type pk:
        @param format:
        @type format:
        @return:
        @rtype:
        """
        question = self.get_object(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk, format=None):
        """
        Creates an Answer on a specific question

        @param request:
        @type request:
        @param pk:
        @type pk:
        @param format:
        @type format:
        @return:
        @rtype:
        """
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


    class AnswerList(APIView):
        """
        API for Answers
        """

        def get(self, request, format=None):
            """
            Returns answers of a Survey
            @param request:
            @type request:
            @param format:
            @type format:
            @return:
            @rtype:
            """
            raise NotImplementedError

    class StarRatingDetail(APIView):
        """
        API for StarRating
        """

        def post(self, request):
            """
            Creates Star Rating Record for a User
            @param request:
            @type request:
            @return:
            @rtype:
            """
            raise NotImplementedError







