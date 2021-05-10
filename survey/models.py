from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group

# Create your models here.


def default_expiration():
    return timezone.now() + timezone.timedelta(days=10)


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Survey(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through='SurveyToUser')
    groups = models.ManyToManyField(Group, through='SurveyToGroup')
    pub_date = models.DateTimeField(default=timezone.now)
    exp_date = models.DateTimeField(default=default_expiration)
    period = models.DurationField(default=None, null=True, blank=True)

    @property
    def get_questions(self):
        return self.question_set.all()

    def __str__(self):
        return f'{self.name}: {self.description}'


class Question(models.Model):
    TEXT = 'text'
    NUMBER = 'number'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    RADIO = 'radio'
    CHECKBOX = 'checkbox'

    SURVEY_QUESTION_TYPES_CHOICES = [
        (TEXT, 'text'),
        (NUMBER, 'number'),
        (SELECT, 'select'),
        (SELECT_MULTIPLE, 'select-multiple'),
        (RADIO, 'radio'),
        (CHECKBOX, 'checkbox'),
    ]

    text = models.TextField()
    required = models.BooleanField(default=True)
    survey = models.ForeignKey(Survey, blank=False, null=False, on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=50,
        choices=SURVEY_QUESTION_TYPES_CHOICES,
        default=TEXT,
    )
    choices = models.TextField(blank=True, null=True)
    other = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Question: {self.text} of survey {self.survey.name}'


class Answer(models.Model):
    text = models.TextField(blank=True)
    question = models.ForeignKey(Question, blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'Answer: {self.text} to the Question {self.question.text} ' \
               f'given by user: {self.user.name} for survey {self.question.survey.name}'


class SurveyToUser(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, blank=False, null=False, on_delete=models.CASCADE, related_name='user_survey')
    completed = models.BooleanField(default=False, null=False)
    completion_date = models.DateTimeField(default=None, null=True, blank=True)


class SurveyToGroup(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, blank=False, null=False, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False, null=False)
    completion_date = models.DateTimeField(default=None, null=True, blank=True)


class StarRating(models.Model):
    text = models.TextField(blank=True, null=False, default=None)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    completed = models.DateTimeField(blank=True, null=True, default=None)

