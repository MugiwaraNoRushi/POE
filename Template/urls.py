from django.urls import path
from Template.views import *

urlpatterns = [
    path('add/template/',create_Template,name = 'create a template'),
    path('delete/template/',delete_Template,name = 'delete a template'),
    path('get/all/templates/',get_all_Templates,name = 'fetch all templates'),
    path('update/template/',update_template,name = 'update a template'),
    path('add/section/',create_Section,name = 'create a  section'),
    path('delete/section/',delete_Section,name = 'delete a section'),
    path('update/section/',update_Section,name = 'update a section'),
    path('get/all/sections',get_all_Sections,name = 'fetch all sections')
]