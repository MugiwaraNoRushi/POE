import json
from Exams.models import *
from Users.models import *
from Template.models import *
from Questions.models import *
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from POE.authentication import authenticate

@csrf_exempt
def create_exam(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'exam_name','exam_duration','group_id','template_id','show_result','result_timestamp','is_enable','exam_enable_time','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                group = Master_Groups.objects.get(id = data['group_id'],is_available = True)
                template = Master_Template.objects.get(id = data['template_id'],is_available = True)
                exam = Master_Exam.objects.create(
                    exam_name = data['exam_name'],
                    exam_duration = data['exam_duration'],
                    group = group,
                    template = template,
                    show_result_immediately = data['show_result'],
                    result_timestamp = data['result_timestamp'],
                    is_enable = data['is_enable'],
                    exam_enable_time = data['exam_enable_time']
                )
                exam.save()
                resp = Response(200,'exam created successfully')
                return JsonResponse(resp,status = 200)
            except Master_Template.DoesNotExist:
                resp = Response(203,'Template doesnot exists')
                return JsonResponse(resp,status  = 200)
            except Master_Groups.DoesNotExist:
                resp = Response(203,'Group doesnot exists')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

#decide the parameters to return
@csrf_exempt
def get_exam(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                exam = Master_Exam.objects.get(id = data['id'])
                return JsonResponse(get_exam_dict(exam),status = 200)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def get_all_exams(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            exams_arr = []
            exams_dict = {'data':exams_arr}
            try:
                exams = Master_Exam.objects.all()
                for exam in exams:
                    exams_arr.append(get_exam_dict(exam))
                return JsonResponse(exams_dict,status = 200)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def update_exam(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'id','exam_name','exam_duration','group_id','template_id','show_result','result_timestamp','is_enable','exam_enable_time','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                group = Master_Groups.objects.get(id = data['group_id'],is_available = True)
                template = Master_Template.objects.get(id = data['template_id'],is_available = True)
                exam = Master_Exam.objects.get(id = data['id'],is_available = True)
                exam.exam_name = data['exam_name']
                exam.exam_duration = data['exam_duration']
                exam.group = group
                exam.template = template
                exam.show_result_immediately = data['show_result']
                exam.result_timestamp = data['result_timestamp']
                exam.is_enable = data['is_enable']
                exam.exam_enable_time = data['exam_enable_time']
                exam.save()
                resp = Response(200,'exam upadeted successfully')
                return JsonResponse(resp,status = 200)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status  = 200)
            except Master_Template.DoesNotExist:
                resp = Response(203,'Template doesnot exists')
                return JsonResponse(resp,status  = 200)
            except Master_Groups.DoesNotExist:
                resp = Response(203,'Group doesnot exists')
                return JsonResponse(resp,status  = 200)
       
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def delete_exam(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                exam = Master_Exam.objects.get(id = data['id'],is_available = True)
                exam.is_available = False
                exam.save()
                resp = Response(200,'exam deleted successfully')
                return JsonResponse(resp,status = 200)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status  = 200)
       
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)



@csrf_exempt
def delete_user_test(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                user_test_status = User_Test_Status.objects.get(id = data['id'])
                user_test_status.delete()
                resp = Response(200,'user_test_status deleted successfully')
                return JsonResponse(resp,status = 200)
            except User_Test_Status.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status  = 200)
       
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)



@csrf_exempt
def get_all_exams_user(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'user_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                user = Master_Users.objects.get(id = data['user_id'])
                group_mappings = User_Group_Mapping.objects.filter(user = user)
            except Master_Users.DoesNotExist:
                resp = Response(204,'User doesnot exist ')
                return JsonResponse(resp,status  = 200)
            except User_Group_Mapping.DoesNotExist:
                resp = Response(204,'user and group do not match')
                return JsonResponse(resp,status  = 200)
            exams_arr = []
            exams_dict = {'data':exams_arr}
            for group_mapping in group_mappings:
                try:
                    group = group_mapping.group
                    exams = Master_Exam.objects.filter(group = group)
                except Master_Exam.DoesNotExist:
                    pass
                for exam in exams:
                    temp_dict = get_exam_dict(exam)
                    try:
                        user_test = User_Test_Status.objects.get(exam = exam,user = user)
                        temp_dict['status'] = user_test.status
                    except User_Test_Status.DoesNotExist:
                        temp_dict['status'] = 1
                    exams_arr.append(temp_dict)
            return JsonResponse(exams_dict,status = 200)
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_exam_perman(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                exam = Master_Exam.objects.get(id = data['id'],is_available = True)
                exam.delete()
                resp = Response(200,'exam deleted successfully')
                return JsonResponse(resp,status = 200)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status  = 200)
       
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)




#--------------------------------UTILS -----------------------------------------------------

def get_exam_dict(exam):

    group = exam.group
    template = exam.template
    admin = group.group_admin

    exam_dict = {
        'id':exam.id,
        'name':exam.exam_name,
        'duration':exam.exam_duration,
        'show_result_immediately':exam.show_result_immediately,
        'result_timestamp':exam.result_timestamp,
        'exam_enable_time': exam.exam_enable_time,
        'is_enable':exam.is_enable,
        'is_available':exam.is_available,
        'group':{
            "id":group.id,
            "group_name":group.group_name,
            'group_admin_id':admin.id,
            'is_available':group.is_available
        },
        "template":{
            'id':template.id,
            'name':template.template_name,
            'marks': template.template_marks,
            'duration': template.template_duration,
            'is_available': template.is_available
        }
    }
    return exam_dict
