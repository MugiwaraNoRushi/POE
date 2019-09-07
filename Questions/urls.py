from django.urls import path
from Questions.views import *

urlpatterns = [
    path('add/question/',add_question,name = "add question with options"),
    path('delete/question/',delete_question,name = "delete question with options")
]