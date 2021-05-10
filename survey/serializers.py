from rest_framework import serializers
from django.contrib.auth.models import User, Group
from survey.models import Survey, SurveyToUser, SurveyToGroup, Category, Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'



class PostQuestionSerializer(serializers.ModelSerializer):
    question_type = serializers.ChoiceField(Question.SURVEY_QUESTION_TYPES_CHOICES)
    class Meta:
        model = Question
        exclude = ['id', 'survey']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class SurveyToUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SurveyToUser
        fields = ['user', 'completed', 'completion_date']


class SurveyToGroupSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = SurveyToGroup
        fields = ['group', 'completed', 'completion_date']


class SurveySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    users = SurveyToUserSerializer(many=True, source='user_survey')
    groups = SurveyToGroupSerializer(many=True, source='surveytogroup_set.all')

    class Meta:
        model = Survey
        fields = [
            'id',
            'name',
            'description',
            'category_name',
            'users',
            'groups',
            'pub_date',
            'exp_date',
            'period'
        ]


class PostSurveySerializer(serializers.Serializer):
    """
    Serializer for Survey post request/creating new survey.
    """
    name = serializers.CharField(max_length=255, required=True, help_text="Name of the Survey")
    description = serializers.CharField(allow_null=True, help_text="Description of the Survey")
    category = serializers.IntegerField(required=True, help_text="Category of the Survey")
    user_emails = serializers.ListField(required=False, help_text="List of emails of users to add to the Survey")
    groups = serializers.ListField(required=False,help_text="List of Groups to add to the Survey")
    questions = PostQuestionSerializer(many=True, required=False, help_text="List of question objects to create along with the survey")
    pub_date = serializers.DateTimeField(required=True, help_text="Date that the Survey should be published")
    exp_date = serializers.DateTimeField(required=False, help_text="Date that the survey stops from publishing.")
    period = serializers.DurationField(required=False, help_text="Interval that the Survey is displayed.")

    # def validate(self, data):
    #     """
    #     Validation of user_emails and groups.
    #     Check that at least one of them is provided
    #     """
    #     # emails = data['user_emails']
    #     # groups = data['groups']
    #     # if not emails and not groups:
    #     raise  serializers.ValidationError("at least one of user_emails or groups is required")
    #     #return data


class PostAddQuestionSerializer(serializers.Serializer):
    """
    Serializer to add a new question to an exiting Survey
    Accepting list of question objects
    """
    questions = PostQuestionSerializer(many=True, required=True, help_text='list of new question objects to be added to a survey')


class AnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(required=True, help_text="Users anwser to the question")
    user_email = serializers.EmailField(required=True, help_text='Email of the user that answered the Question')