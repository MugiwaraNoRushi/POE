import json
from Topics.models import Master_SubTopic
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Template.models import *

# make a duplicate template
@csrf_exempt
def create_Template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'name','marks','duration'}.issubset(data.keys()):
            template = Master_Template.objects.create(
                template_name = data['name'],
                template_marks = data['marks'],
                template_duration = data['duration']
            )
            template.save()
            resp = Response(200,'template created successfully')
            return JsonResponse(resp,status = 200)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def delete_Template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:
                template = Master_Template.objects.get(id = data['id'],is_available = True)
                template.is_available = False
                template.save()
                resp = Response(200,'template deleted successfully')
                return JsonResponse(resp, status = 200)
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def get_all_Templates(request):
    if request.method == 'POST':
        templates_arr = []
        templates_dict = {'data':templates_arr}
        temp = {}
        templates = Master_Template.objects.filter(is_available = True)
        for template in templates:
            temp = {
                'id':template.id,
                'name':template.template_name,
                'marks':template.template_marks,
                'duration':template.template_duration
            }
            templates_arr.append(temp)
        return JsonResponse(templates_dict,status = 200)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def update_template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','name','marks','duration'}.issubset(data.keys()):
            try:
                template = Master_Template.objects.get(id = data['id'],is_available = True)
                template.template_name = data['name'],
                template.template_duration = data['duration'],
                template.template_marks = data['marks']
                template.save()
                resp = Response(200,'template updated successfully')
                return JsonResponse(resp, status = 200)
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def create_Section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'name','marks','duration','template_id','negative_marks'}.issubset(data.keys()):
            try:
                template = Master_Template.objects.get(id = data['template_id'],is_available = True)
                section = Master_Section.objects.create(
                    section_name = data['name'],
                    section_marks = data['marks'],
                    section_duration = data['duration'],
                    template = template,
                    negative_marks = data['negative_marks']
                )
                section.save()
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status = 203)
            resp = Response(200,'section created successfully')
            return JsonResponse(resp,status = 200)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def delete_Section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:
                section = Master_Section.objects.get(id = data['id'],is_available = True)
                section.is_available = False
                section.save()
                resp = Response(200,'section deleted successfully')
                return JsonResponse(resp, status = 200)
            except:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def update_Section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','name','marks','duration','template_id','negative_marks'}.issubset(data.keys()):
            try:
                section = Master_Section.objects.get(id = data['id'],is_available = True)
                section.section_marks = data['marks']
                section.section_duration = data['duration']
                section.section_name = data['name']
                section.negative_marks = data['negative_marks']
                template = Master_Template.objects.get(id = data['template_id'])
                section.template = template
                section.save()
                resp = Response(200,'section updated successfully')
                return JsonResponse(resp, status = 200)
            except Master_Section.DoesNotExist:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status = 203)
            except Master_Template.DoesNotExist:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def get_all_Sections(request):
    if request.method == 'POST':
        sections_arr = []
        sections_dict = {'data':sections_arr}
        temp = {}
        sections = Master_Section.objects.filter(is_available = True)
        for section in sections:
            template = section.template
            temp = {
                'id':section.id,
                'name':section.section_name,
                'marks':section.section_marks,
                'duration':section.section_duration,
                'negative_marks':section.negative_marks,
                'template':{
                    'id':template.id,
                    'name':template.template_name,
                    'marks':template.template_marks,
                    'duration':template.template_duration
                }
            }
            sections_arr.append(temp)
        return JsonResponse(sections_dict,status = 200)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def create_template_section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'section_id','subtopic_id','difficulty_id','no_question'}.issubset(data.keys()):
            try:
                section = Master_Section.objects.get(id = data['section_id'],is_available = True)
                subtopic = Master_SubTopic.objects.get(id = data['subtopic_id'],is_available = True)
                temp_section = Template_Section.objects.create(
                    section =section,
                    subtopic = subtopic,
                    difficulty_id = data['difficulty_id'],
                    no_questions = data['no_question'] 
                )
                temp_section.save()
            except Master_Section.DoesNotExist:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status = 203)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203, 'subtopic doesnot exist')
                return JsonResponse(resp,status = 203)
            resp = Response(200,'template_section created successfully')
            return JsonResponse(resp,status = 200)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def update_template_section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','section_id','subtopic_id','difficulty_id','no_question'}.issubset(data.keys()):
            try:
                section = Master_Section.objects.get(id = data['section_id'],is_available = True)
                subtopic = Master_SubTopic.objects.get(id = data['subtopic_id'],is_available = True)
                temp_section = Template_Section.objects.get(id = data['id'])
                temp_section.section =section
                temp_section.subtopic = subtopic
                temp_section.difficulty_id = data['difficulty_id']
                temp_section.no_questions = data['no_question'] 
                temp_section.save()
            except Template_Section.DoesNotExist:
                resp = Response(203,'Template_Section doesnot exist')
                return JsonResponse(resp,status = 203)
            except Master_Section.DoesNotExist:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status = 203)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203, 'subtopic doesnot exist')
                return JsonResponse(resp,status = 203)
            resp = Response(200,'template_section updated successfully')
            return JsonResponse(resp,status = 200)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)
#update in future
@csrf_exempt
def get_all_template_sections(request):
    if request.method == 'POST':
        template_sections_arr = []
        template_sections_dict = {'data':template_sections_arr}
        temp = {}
        template_sections = Template_Section.objects.filter()
        for template_section in template_sections:
            section = template_section.section
            subtopic = template_section.subtopic
            temp = {
                'id':template_section.id,
                'difficulty_id':template_section.difficulty_id,
                'section':{
                    'id':section.id,
                    },
                'subtopic':{
                    'id':subtopic.id,
                }    
            }
            template_sections_arr.append(temp)
        return JsonResponse(template_sections_dict,status = 200)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

@csrf_exempt
def delete_section_template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:

                temp_section = Template_Section.objects.get(id = data['id'])
                temp_section.delete()
            except Template_Section.DoesNotExist:
                resp = Response(203,'Template_Section doesnot exist')
                return JsonResponse(resp,status = 203)
            resp = Response(200,'template_section deleted successfully')
            return JsonResponse(resp,status = 200)
        else:
            resp = Response(204,'Wrong key value')
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Wrong Request')
        return JsonResponse(resp, status = 405)

