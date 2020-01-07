from django.urls import path
from Questions.views import *
from Questions.test_question import *

urlpatterns = [
    path('add/question/',add_question,name = "add question with options"),
    path('delete/question/',delete_question,name = "delete question with options"),
    #path('activate/question/',activate_question,name = "activate question with options"),
    path('change/question/',update_question,name = 'change question with all options and correct options'),
    path('get/question/',get_question,name = 'get question basis of id'),
    path('get/all/questions/',get_all_questions,name = 'get all questions basis of subtopic'),
    path('get/all/questions/subtopic/',get_all_questions_subtopic,name = 'get all questions basis of subtopic'),
    path('add/questionssss/admin/test/',add_questions, name = 'add many questions for testing purpose')
]