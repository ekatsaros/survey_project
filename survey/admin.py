from django.contrib import admin
from django.contrib.auth.models import User, Group

# Register your models here.

from .models import Survey, Question, Answer, SurveyToUser, SurveyToGroup, Category

#admin.site.register(Survey)
#admin.site.register(Question)
#admin.site.register(Answer)
# admin.site.register(SurveyToUser)
# admin.site.register(SurveyToGroup)

class SurveyToUserInline(admin.TabularInline):
    model = SurveyToUser
    extra=1

class SurveyToGroupInline(admin.TabularInline):
    model = SurveyToGroup
    extra=1

class QuestionInline(admin.TabularInline):
    model = Question
    extra=1

class SurveyAdmin(admin.ModelAdmin):
    inlines = (SurveyToUserInline, SurveyToGroupInline, QuestionInline)

class UserAdmin(admin.ModelAdmin):
    inlines = (SurveyToUserInline,)

# class GroupAdmin(admin.ModelAdmin):
#     inlines = (SurveyToGroupInline, )

admin.site.register(Category)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#admin.site.register(Group, GroupAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer)

