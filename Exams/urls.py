from django.urls import path
from Exams.views import *

urlpatterns = [
    path('create/exams/',create_exam,name = 'create exams'),
    path('get/exam/',get_exam,name = 'get a single exam'),
    path('update/exam/',update_exam,name = 'update a exam'),
    path('delete/exam/',delete_exam,name = 'delete a exam')
]