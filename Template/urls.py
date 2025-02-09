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
    path('get/sectionwithtemplate/',get_template_section_id,name = 'get a single template section'),
    path('get/all/sectionwithtemplatesbysection/',get_all_template_section_section_id,name = 'get all sectionwithtemplates by section'),
    path('update/section/marks',update_Section_marks,name = 'update section marks'),
    path('get/all/sections/template/',get_all_Sections_template,name = 'get all sections based on template id'),
    path('delete/template/perm/',delete_Template_perman,name = 'delete template permanently'),
    path('delete/section/perm/',delete_Section_perman,name = 'delete a section permanently')
]
