from django.urls import path
from Questions.views import *

urlpatterns = [
    path('add/question/',add_question,name = "add question with options"),
    path('delete/question/',delete_question,name = "delete question with options"),
    path('change/question/',update_question,name = 'change question with all options and correct options'),
    path('get/all/questions/subtopic/',get_all_questions,name = 'get all questions basis of subtopic')
]