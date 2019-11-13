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
    path('get/all/sections/',get_all_Sections,name = 'fetch all sections'),
    path('add/sectionwithtemplate/',create_template_section,name = 'create a template section'),
    path('update/sectionwithtemplate/',update_template_section,name = 'update a template section'),
    path('get/all/sectionwithtemplates/',get_all_template_sections,name = 'fetch all section with templates'),
    path('delete/sectionwithtemplate/',delete_section_template,name = 'delete a section with template'),
    path('activate/section/',activate_Section,name = 'activate a section'),
    path('activate/template/',activate_Template,name = 'activate a template'),
    path('get/template/',get_Template,name = 'get single template'),
    path('get/section/',get_Section,name = 'get a single section'),
]