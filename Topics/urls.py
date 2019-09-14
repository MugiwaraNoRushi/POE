from django.urls import path
from Topics.views import *



urlpatterns = [
    path('add/topic/',create_topic,name = 'add a topic'),
    path('add/subtopic/',create_subtopic,name = 'add a subtopic'),
    path('get/topic/',get_topic,name = "fetch a topic"),
    path('get/subtopic/',get_subtopic,name = "fetch a subtopic"),
    path('delete/topic/',delete_topic,name = 'delete a topic'),
    path('delete/subtopic/',delete_subtopic,name = 'delete a  subtopic'),
]