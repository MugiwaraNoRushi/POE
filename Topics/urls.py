from django.urls import path
from Topics.views import *



urlpatterns = [
    path('add/topic/',create_topic,name = 'add a topic'),
    path('add/subtopic/',create_subtopic,name = 'add a subtopic'),
    path('get/all/topic/',get_all_topics,name = "fetch a topic"),
    path('get/all/subtopic/',get_all_subtopics,name = "fetch a subtopic"),
    path('delete/topic/',delete_topic,name = 'delete a topic'),
    path('delete/subtopic/',delete_subtopic,name = 'delete a  subtopic'),
    path('update/topic/',update_topic,name = 'update a topic'),
    path('update/subtopic/',update_subtopic,name = 'update a subtopic'),
    path('get/topic/',get_topic,name = 'get a topic'),
    path('get/subtopic/',get_subtopic,name = 'get a subtopic'),
    path('activate/topic/',activate_topic,name = 'delete a topic'),
    path('activate/subtopic/',activate_subtopic,name = 'delete a  subtopic'),
]