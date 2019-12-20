import json
from Topics.models import Master_SubTopic
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Template.models import *
from POE.authentication import authenticate
from Questions.models import *

# make a duplicate template
@csrf_exempt
def create_Template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'name','marks','duration','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            template = Master_Template.objects.create(
                template_name = data['name'],
                template_marks = data['marks'],
                template_duration = data['duration']
            )
            template.save()
            resp = Response(200,'template created successfully')
            return JsonResponse(resp,status = 200)
    
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def delete_Template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                template = Master_Template.objects.get(id = data['id'],is_available = True)
                template.is_available = False
                template.save()
                resp = Response(200,'template deleted successfully')
                return JsonResponse(resp, status = 200)
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def get_all_Templates(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            templates_arr = []
            templates_dict = {'data':templates_arr}
            temp = {}
            templates = Master_Template.objects.all()
            for template in templates:
                temp = {
                    'id':template.id,
                    'name':template.template_name,
                    'marks':template.template_marks,
                    'duration':template.template_duration,
                    'is_available':template.is_available
                }
                templates_arr.append(temp)
            return JsonResponse(templates_dict,status = 200)
    
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def update_template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','name','marks','duration','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                template = Master_Template.objects.get(id = data['id'])
                template.template_name = data['name']
                template.template_duration = data['duration']
                template.template_marks = data['marks']
                template.save()
                resp = Response(200,'template updated successfully')
                return JsonResponse(resp, status = 200)
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def create_Section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'name','marks','duration','template_id','negative_marks','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
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
                update_marks(section)
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status  = 200)
            resp = Response(200,'section created successfully')
            return JsonResponse(resp,status = 200)
    
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def delete_Section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                section = Master_Section.objects.get(id = data['id'],is_available = True)
                section.is_available = False
                section.save()
                update_marks(section)
                resp = Response(200,'section deleted successfully')
                return JsonResponse(resp, status = 200)
            except:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def update_Section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','name','marks','duration','template_id','negative_marks','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                section = Master_Section.objects.get(id = data['id'])
                section.section_marks = data['marks']
                section.section_duration = data['duration']
                section.section_name = data['name']
                section.negative_marks = data['negative_marks']
                template = Master_Template.objects.get(id = data['template_id'])
                section.template = template
                section.save()
                update_marks(section)
                resp = Response(200,'section updated successfully')
                return JsonResponse(resp, status = 200)
            except Master_Section.DoesNotExist:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status  = 200)
            except Master_Template.DoesNotExist:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def update_Section_marks(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','marks','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                section = Master_Section.objects.get(id = data['id'])
                section.section_marks = data['marks']
                section.save()
                update_marks(section)
                resp = Response(200,'section marks and template marks updated successfully')
                return JsonResponse(resp, status = 200)
            except Master_Section.DoesNotExist:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status  = 200)
            except Master_Template.DoesNotExist:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def get_all_Sections(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            sections_arr = []
            sections_dict = {'data':sections_arr}
            temp = {}
            sections = Master_Section.objects.all()
            for section in sections:
                template = section.template
                temp = {
                    'id':section.id,
                    'name':section.section_name,
                    'marks':section.section_marks,
                    'duration':section.section_duration,
                    'negative_marks':section.negative_marks,
                    'is_available':section.is_available,
                    'template':{
                        'id':template.id,
                        'name':template.template_name,
                        'marks':template.template_marks,
                        'duration':template.template_duration,
                        'is_available':template.is_available,
                    }
                }
                sections_arr.append(temp)
            return JsonResponse(sections_dict,status = 200)
    
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def get_all_Sections_template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','template_id'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                template = Master_Template.objects.get(id = data['template_id'])
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status  = 200)
            sections_arr = []
            sections_dict = {'data':sections_arr}
            temp = {}
            try:
                sections = Master_Section.objects.filter(template = template)
            except:
                return JsonResponse(sections_dict,status = 200)
            for section in sections:
                template = section.template
                temp = {
                    'id':section.id,
                    'name':section.section_name,
                    'marks':section.section_marks,
                    'duration':section.section_duration,
                    'negative_marks':section.negative_marks,
                    'is_available':section.is_available,
                    'template':{
                        'id':template.id,
                        'name':template.template_name,
                        'marks':template.template_marks,
                        'duration':template.template_duration,
                        'is_available':template.is_available,
                    }
                }
                sections_arr.append(temp)
            return JsonResponse(sections_dict,status = 200)
    
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)


@csrf_exempt
def create_template_section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'section_id','subtopic_id','difficulty_id','no_question'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                section = Master_Section.objects.get(id = data['section_id'],is_available = True)
                subtopic = Master_SubTopic.objects.get(id = data['subtopic_id'],is_available = True)
                if check_template_section(subtopic,data['difficulty_id'],data['no_question']):
                    temp_section = Template_Section.objects.create(
                        section =section,
                        subtopic = subtopic,
                        difficulty_id = data['difficulty_id'],
                        no_questions = data['no_question']
                    )
                    temp_section.save()
                    update_section_marks(section)
                    resp = Response(200,'template_section created successfully')
                    return JsonResponse(resp,status = 200)
                else:
                    resp = Response(203,'not enough questions available')
                    return JsonResponse(resp,status  = 200)
            except Master_Section.DoesNotExist:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status  = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203, 'subtopic doesnot exist')
                return JsonResponse(resp,status  = 200)
            
    
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def update_template_section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','id','section_id','subtopic_id','difficulty_id','no_question'}.issubset(data.keys())  and authenticate(data['auth_key']):
            try:
                section = Master_Section.objects.get(id = data['section_id'],is_available = True)
                subtopic = Master_SubTopic.objects.get(id = data['subtopic_id'],is_available = True)
                if check_template_section(subtopic,data['difficulty_id'],data['no_question']):
                    temp_section = Template_Section.objects.get(id = data['id'])
                    temp_section.section =section
                    temp_section.subtopic = subtopic
                    temp_section.difficulty_id = data['difficulty_id']
                    temp_section.no_questions = data['no_question']
                    temp_section.save()
                    update_section_marks(section)
                    resp = Response(200,'template_section updated successfully')
                    return JsonResponse(resp,status = 200)
                else:
                    resp = Response(203,'not enough questions available')
                    return JsonResponse(resp,status  = 200)
            except Template_Section.DoesNotExist:
                resp = Response(203,'Template_Section doesnot exist')
                return JsonResponse(resp,status  = 200)
            except Master_Section.DoesNotExist:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status  = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203, 'subtopic doesnot exist')
                return JsonResponse(resp,status  = 200)
            
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)


@csrf_exempt
def get_all_template_sections(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            template_sections_arr = []
            template_sections_dict = {'data':template_sections_arr}
            template_sections = Template_Section.objects.filter()
            for template_section in template_sections:
                template_sections_arr.append(get_template_section_dict(template_section))
            return JsonResponse(template_sections_dict,status = 200)
    
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def get_template_section_id(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','id'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                template_section =Template_Section.objects.get(id = data['id'])
                return JsonResponse(get_template_section_dict(template_section),status = 200)
            except Template_Section.DoesNotExist:
                resp = Response(203,'template_section doestnot exists')
                return JsonResponse(resp,status  = 200)
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)


@csrf_exempt
def get_all_template_section_section_id(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','section_id'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                section = Master_Section.objects.get(id = data['section_id'])
                template_sections_arr = []
                template_sections_dict = {'data':template_sections_arr}
                template_sections = Template_Section.objects.filter(section = section)
                for template_section in template_sections:
                    template_sections_arr.append(get_template_section_dict(template_section))
                return JsonResponse(template_sections_dict,status = 200)
            except Template_Section.DoesNotExist:
                resp = Response(203,'template_section doestnot exists')
                return JsonResponse(resp,status  = 200)
            except Master_Section.DoesNotExist:
                resp = Response(203,'section doestnot exists')
                return JsonResponse(resp,status  = 200)
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)


@csrf_exempt
def delete_section_template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:

                temp_section = Template_Section.objects.get(id = data['id'])
                section = temp_section.section
                temp_section.delete()
                update_section_marks(section)
            except Template_Section.DoesNotExist:
                resp = Response(203,'Template_Section doesnot exist')
                return JsonResponse(resp,status  = 200)
            resp = Response(200,'template_section deleted successfully')
            return JsonResponse(resp,status = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)


@csrf_exempt
def activate_Template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                template = Master_Template.objects.get(id = data['id'],is_available = False)
                template.is_available = True
                template.save()
                resp = Response(200,'template updated successfully')
                return JsonResponse(resp, status = 200)
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)


@csrf_exempt
def activate_Section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                section = Master_Section.objects.get(id = data['id'],is_available = False)
                section.is_available = True
                section.save()
                update_marks(section)
                resp = Response(200,'section updated successfully')
                return JsonResponse(resp, status = 200)
            except:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status  = 200)
       
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def get_Section(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                section = Master_Section.objects.get(id = data['id'])
                template = section.template
                section_dict = {
                    'id':section.id,
                    'name':section.section_name,
                    'marks':section.section_marks,
                    'duration':section.section_duration,
                    'negative_marks':section.negative_marks,
                    'is_available':section.is_available,
                    'template':{
                        'id':template.id,
                        'name':template.template_name,
                        'marks':template.template_marks,
                        'duration':template.template_duration,
                        'is_available':template.is_available,
                    }
                }
                return JsonResponse(section_dict, status = 200)
            except:
                resp = Response(203,'section doesnot exist')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

@csrf_exempt
def get_Template(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                template = Master_Template.objects.get(id = data['id'])
                temp = {
                'id':template.id,
                'name':template.template_name,
                'marks':template.template_marks,
                'duration':template.template_duration,
                'is_available':template.is_available
                }
                return JsonResponse(temp, status = 200)
            except:
                resp = Response(203,'template doesnot exist')
                return JsonResponse(resp,status = 200)
        
    resp = Response(405,'Wrong Request')
    return JsonResponse(resp, status = 405)

    #------------------UTILS---------------------------------------------------------------

def get_template_section_dict(template_section):
    section = template_section.section
    template = section.template
    subtopic = template_section.subtopic
    topic = subtopic.topic
    temp = {
        'id':template_section.id,
        'difficulty_id':template_section.difficulty_id,
        'no_questions':template_section.no_questions,
        'section':{
            'id':section.id,
            'name':section.section_name,
            'marks':section.section_marks,
            'duration':section.section_duration,
            'negative_marks':section.negative_marks,
            'is_available' : section.is_available,
            'template':{
                'id':template.id,
                'name':template.template_marks,
                'marks':template.template_marks,
                'duration':template.template_duration,
                'is_available':template.is_available,
                }
            },
        'subtopic':{
            'id':subtopic.id,
            'text':subtopic.subtopic_text,
            'is_available':subtopic.is_available,
            'topic':{
                'id':topic.id,
                'text':topic.topic_text,
                'is_available':topic.is_available
            }
        }
    }
    return temp


def update_marks(section):
    template = section.template
    t_marks = 0
    try:
        sections_arr = Master_Section.objects.filter(template = template,is_available = True)
    except:
        pass
    for section in sections_arr:
        t_marks = t_marks + section.section_marks    
    template.template_marks = t_marks
    template.save()

def update_section_marks(section):
    marks = 0
    try:
        template_section_arr = Template_Section.objects.filter(section =section)
        for template_section in template_section_arr:
            template_section_marks = template_section.no_questions * template_section.difficulty_id
            marks = marks + template_section_marks
    except:
        pass
    section.section_marks = marks
    section.save()
    update_marks(section)

def check_template_section(subtopic,difficulty_id,no_questions):
    questions = Master_Question.objects.filter(subtopic = subtopic,difficulty = difficulty_id)
    if len(questions)>=no_questions:
        return True
    else:
        return False