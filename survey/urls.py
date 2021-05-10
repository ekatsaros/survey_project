from django.urls import re_path, path

from survey import views

urlpatterns = [
    path('surveys/', views.SurveyList.as_view(), name='survey-list'),
    path('surveys/categories/', views.CategoryList.as_view()),
    path('surveys/<int:pk>/', views.SurveyDetail.as_view()),
    path('surveys/<int:pk>/questions/', views.SurveyDetail.as_view(), name='survey_questions'),
    path('questions/<int:pk>/', views.QuestionDetail.as_view())
]
