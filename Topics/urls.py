from django.urls import path
from Topics.views import *



urlpatterns = [
    path('add/topic/',create_topic,name = 'add a topic'),
    path('add/subtopic/',create_subtopic,name = 'add a subtopic'),
    path('get/all/topic/',get_all_topics,name = "fetch a topic"),
    path('get/all/subtopic/',get_all_subtopics,name = "fetch a subtopic"),
    path('delete/topic/',delete_topic,name = 'delete a topic'),
    path('delete/subtopic/',delete_subtopic,name = 'delete a  subtopic'),
]