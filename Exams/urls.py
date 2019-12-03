from django.urls import path
from Exams.views import *
from Exams.heart import *

urlpatterns = [
    path('create/exam/',create_exam,name = 'create exam'),
    path('get/all/exams/',get_all_exams,name = 'get a list of exam'),
    path('get/exam/',get_exam,name = 'get a single exam'),
    path('update/exam/',update_exam,name = 'update a exam'),
    path('delete/exam/',delete_exam,name = 'delete a exam'),
    path('create/user/test/status/',create_user_test,name = 'create a user test status'),
    path('update/user/test/status/',update_user_test,name = 'update a user test status'),
    path('delete/user/test/status/',delete_user_test,name = 'delete a user test status'),
    path('start/exam/',assign_questions_to_exam,name = 'start exam ; doesnot matter for first time or aftermore'),
    path('scroll/through/exam/',scroll_through_exam,name = 'for pressing next button')
]
