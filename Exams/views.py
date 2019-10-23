import json
from Exams.models import *
from Users.models import *
from Template.models import *
from Questions.models import *
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_exam(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'exam_name','exam_duration','group_id','template_id','show_result','result_timestamp','is_enable','exam_enable_time'}.issubset(data.keys()):
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
                return JsonResponse(resp,status = 203)
            except Master_Groups.DoesNotExist:
                resp = Response(203,'Group doesnot exists')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value pair')
            return JsonResponse(resp,status = 204)


#decide the parameters to return 
@csrf_exempt
def get_exam(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:
                exam = Master_Exam.objects.get(id = data['id'],is_available = True)
                group = exam.group
                template = exam.template 
                admin = group.group_admin
                exam_dict = {
                    'name':exam.exam_name,
                    'duration':exam.exam_duration,
                    'show_result_immediately':exam.show_result_immediately,
                    'result_timestamp':exam.result_timestamp,
                    'is_enable':exam.is_enable,
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
                return JsonResponse(exam_dict,status = 200)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value pair')
            return JsonResponse(resp,status = 204)

@csrf_exempt
def update_exam(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'id','exam_name','exam_duration','group_id','template_id','show_result','result_timestamp','is_enable','exam_enable_time'}.issubset(data.keys()):
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
                return JsonResponse(resp,status = 203)
            except Master_Template.DoesNotExist:
                resp = Response(203,'Template doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Groups.DoesNotExist:
                resp = Response(203,'Group doesnot exists')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value pair')
            return JsonResponse(resp,status = 204)

@csrf_exempt
def delete_exam(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:
                exam = Master_Exam.objects.get(id = data['id'],is_available = True)
                exam.is_available = False
                exam.save()
                resp = Response(200,'exam deleted successfully')
                return JsonResponse(resp,status = 200)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value pair')
            return JsonResponse(resp,status = 204)

@csrf_exempt
def create_user_test(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'exam_id','user_id','status','duration'}.issubset(data.keys()):
            try:
                exam = Master_Exam.objects.get(id = data['exam_id'])
                user = Master_Users.objects.get(id = data['user_id'])
                user_test_status = User_Test_Status.objects.create(
                    exam = exam,
                    user = user,
                    status = data['status'],
                    duration = data['duration']
                )
                user_test_status.save()
                resp = Response(200,'user_test_status created successfully')
                return JsonResponse(resp,status = 200)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Users.DoesNotExist:
                resp = Response(203,'User doesnot exists')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value pair')
            return JsonResponse(resp,status = 204)
#do u need to update the user ??
@csrf_exempt
def update_user_test(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'id','status','duration'}.issubset(data.keys()):
            try:
                user_test_status = User_Test_Status.objects.get(id = data['id'])
                user_test_status.status = data['status']
                user_test_status.duration = data['duration']
                user_test_status.save()
                resp = Response(200,'user_test_status updated successfully')
                return JsonResponse(resp,status = 200)

            except User_Test_Status.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Users.DoesNotExist:
                resp = Response(203,'User doesnot exists')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value pair')
            return JsonResponse(resp,status = 204)

@csrf_exempt
def delete_user_test(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:
                user_test_status = User_Test_Status.objects.get(id = data['id'])
                user_test_status.delete()
                resp = Response(200,'user_test_status deleted successfully')
                return JsonResponse(resp,status = 200)
            except User_Test_Status.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204,'Wrong key value pair')
            return JsonResponse(resp,status = 204)

#do I have to create an activate method for exams, it does not make sense!!!!
#what to do with remaining tables
#dynamic things remain