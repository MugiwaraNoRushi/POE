import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timezone,timedelta
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from Users.models import *
from Users.utils import *
from POE.authentication import authenticate
from pytz import timezone
from Users.views import get_user_dict

@csrf_exempt
def create_subs(request):
    if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','subs_type','plan_name','count'}.issubset(data.keys()) and authenticate(data['auth_key']):
                    subs_master = Master_Subscription.objects.create(
                        subscription_type = data['subs_type'],
                        plan_name = data['plan_name'],
                        count_or_no_days = data['count']
                    )
                    resp = Response(200,"Subscription created successfully")
                    return JsonResponse(resp,status = 200)

    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def update_subs(request):
    if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','subs_id','subs_type','plan_name','count'}.issubset(data.keys()) and authenticate(data['auth_key']):
                    try:
                        subs_master = Master_Subscription.objects.get(id = data['subs_id'],is_available = True)
                        subs_master.plan_name = data['plan_name']
                        subs_master.subs_type = data['subs_type']
                        subs_master.count_or_no_days = data['count']
                        subs_master.save()
                        resp = Response(200,'Subscription updated successfully')
                        return JsonResponse(resp,status = 200)
                    except Master_Subscription.DoesNotExist:
                        resp = Response(203,"Subscription doesnot exists")
                        return JsonResponse(resp,status = 200)
                    resp = Response(200,"Subscription created successfully")
                    return JsonResponse(resp,status = 200)

    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_subs(request):
    if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','subs_id','subs_type','plan_name','count'}.issubset(data.keys()) and authenticate(data['auth_key']):
                    try:
                        subs_master = Master_Subscription.objects.get(id = data['subs_id'],is_available = True)
                        subs_master.is_available = False
                        subs_master.save()
                        resp = Response(200,'Subscription updated successfully')
                        return JsonResponse(resp,status = 200)
                    except Master_Subscription.DoesNotExist:
                        resp = Response(203,"Subscription doesnot exists")
                        return JsonResponse(resp,status = 200)
                    resp = Response(200,"Subscription created successfully")
                    return JsonResponse(resp,status = 200)

    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def activate_subs(request):
    if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','subs_id','subs_type','plan_name','count'}.issubset(data.keys()) and authenticate(data['auth_key']):
                    try:
                        subs_master = Master_Subscription.objects.get(id = data['subs_id'],is_available = False)
                        subs_master.is_available = True
                        subs_master.save()
                        resp = Response(200,'Subscription updated successfully')
                        return JsonResponse(resp,status = 200)
                    except Master_Subscription.DoesNotExist:
                        resp = Response(203,"Subscription doesnot exists")
                        return JsonResponse(resp,status = 200)
                    resp = Response(200,"Subscription created successfully")
                    return JsonResponse(resp,status = 200)

    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)
        

@csrf_exempt
def delete_subs_perman(request):
    if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','subs_id','subs_type','plan_name','count'}.issubset(data.keys()) and authenticate(data['auth_key']):
                    try:
                        subs_master = Master_Subscription.objects.get(id = data['subs_id'])
                        subs_master.delete()
                        resp = Response(200,'Subscription updated successfully')
                        return JsonResponse(resp,status = 200)
                    except Master_Subscription.DoesNotExist:
                        resp = Response(203,"Subscription doesnot exists")
                        return JsonResponse(resp,status = 200)
                    resp = Response(200,"Subscription created successfully")
                    return JsonResponse(resp,status = 200)

    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def get_subs(request):
    if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','subs_id'}.issubset(data.keys()) and authenticate(data['auth_key']):
                    try:
                        subs_master = Master_Subscription.objects.get(id = data['subs_id'])
                        return JsonResponse(get_subs_dict(subs_master),status = 200)
                    except Master_Subscription.DoesNotExist:
                        resp = Response(203,"Subscription doesnot exists")
                        return JsonResponse(resp,status = 200)

    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def get_all_subs(request):
    if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                    subs_master_arr = Master_Subscription.objects.all()
                    arr_dict = []
                    data_dict = {
                        'data':arr_dict
                    }
                    for subs_master in subs_master_arr:
                        arr_dict.append(get_subs_dict(subs_master))
                    return JsonResponse(data_dict,status = 200)
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

#
@csrf_exempt
def create_subs_users(request):
    if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','user_id','subs_id'}.issubset(data.keys() and authenticate(data['auth_key'])):
                    try:
                        user = Master_Users.objects.get(id = data['user_id'])
                        subs_master = Master_Subscription.objects.get(id = data['subs_id'])
                        if subs_master.subscription_type == 2:
                            subs_user_mapping = User_Subscription_Mapping.objects.create(
                                subscription = subs_master,
                                user = user,
                                start_date = None,
                                end_date = None,
                                exam_count = subs_master.count_or_no_days
                            )
                        elif subs_master.subscription_type == 1:
                            today = datetime.now(timezone('Asia/Kolkata'))
                            end_date = today + timedelta(days = subs_master.count_or_no_days)
                            subs_user_mapping = User_Subscription_Mapping.objects.create(
                                subscription = subs_master,
                                user = user,
                                start_date = today,
                                end_date = end_date,
                                exam_count = None
                            )
                        resp = Response(200,"Subscription applied !")
                        return JsonResponse(resp,status = 200)
                    except Master_Users.DoesNotExist:
                        resp = Response(203,"User doesnot exists")
                        return JsonResponse(resp,status = 200)
                    except Master_Subscription.DoesNotExist:
                        resp = Response(203,"Subscription doesnot exists")
                        return JsonResponse(resp,status = 200)
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def get_user_subs(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','id'}.issubset(data.keys() and authenticate(data['auth_key'])):
            try:
                user_subs = User_Subscription_Mapping.objects.get(id =data['id'])
                user = user_subs.user
                if user_subs.start_date == None:
                    start = 0
                    end = 0
                    count = user_subs.count
                else:
                    start = user_subs.start_date
                    end = user_subs.end_date
                    count = 0
                user_subs_dict = {
                    "user":get_user_dict(user),
                    "subs":get_subs_dict(user_subs.subscription),
                    "start":start,
                    "end":end,
                    "count":count
                }
                return JsonResponse(user_subs_dict,status = 200)
            except User_Subscription_Mapping.DoesNotExist:
                resp = Response(203,"Subscription doesnot exists")
                return JsonResponse(resp,status = 200)
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)
    
def get_user_subs_user_id(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','user_id'}.issubset(data.keys() and authenticate(data['auth_key'])):
            try:
                user = Master_Users.object.get(id =data['user_id'],is_available = True)
                user_subs_arr = User_Subscription_Mapping.objects.filter(user = user)
                arr_dict = []
                data_dict = {
                    'data':arr_dict,
                    "user":get_user_dict(user)
                }
                for user_subs in user_subs_arr:
                    if user_subs.start_date == None:
                        start = 0
                        end = 0
                        count = user_subs.count
                    else:
                        start = user_subs.start_date
                        end = user_subs.end_date
                        count = 0
                    user_subs_dict = {
                        "subs":get_subs_dict(user_subs.subscription),
                        "start":start,
                        "end":end,
                        "count":count
                    }
                    arr_dict.append(user_subs_dict)
                return JsonResponse(data_dict,status = 200)
            except User_Subscription_Mapping.DoesNotExist:
                resp = Response(203," User doesnot have any Subscriptions")
                return JsonResponse(resp,status = 200)
            except Master_Users.DoesNotExist:
                resp = Response(203,"User doesnot exists")
                return JsonResponse(resp,status = 200)
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)
        

def get_user_subs_subs_id(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','subs_id'}.issubset(data.keys() and authenticate(data['auth_key'])):
            try:
                subscription = Master_Subscription.objects.get(id = data['subs_id'])
                user_subs_arr = User_Subscription_Mapping.objects.filter(subscription = subscription)
                arr_dict = []
                data_dict = {
                    'data':arr_dict,
                    "subscription":get_subs_dict(subscription)
                }
                for user_subs in user_subs_arr:
                    if user_subs.start_date == None:
                        start = 0
                        end = 0
                        count = user_subs.count
                    else:
                        start = user_subs.start_date
                        end = user_subs.end_date
                        count = 0
                    user_subs_dict = {
                        "user":get_user_dict(user_subs.user),
                        "start":start,
                        "end":end,
                        "count":count
                    }
                    arr_dict.append(user_subs_dict)
                return JsonResponse(data_dict,status = 200)
            except User_Subscription_Mapping.DoesNotExist:
                resp = Response(203,"Subscription is not opted by any user")
                return JsonResponse(resp,status = 200)
            except Master_Subscription.DoesNotExist:
                resp = Response(203,"Subscription doesnot exists")
                return JsonResponse(resp,status = 200)
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


def get_user_subs_all(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key'}.issubset(data.keys() and authenticate(data['auth_key'])):
            try:
                user_subs_arr = User_Subscription_Mapping.objects.all()
                arr_dict = []
                data_dict = {
                    'data':arr_dict,
                }
                for user_subs in user_subs_arr:
                    if user_subs.start_date == None:
                        start = 0
                        end = 0
                        count = user_subs.count
                    else:
                        start = user_subs.start_date
                        end = user_subs.end_date
                        count = 0
                    user_subs_dict = {
                        "user":get_user_dict(user_subs.user),
                        "subs":get_subs_dict(user_subs.subscription),
                        "start":start,
                        "end":end,
                        "count":count
                    }
                    arr_dict.append(user_subs_dict)
                return JsonResponse(data_dict,status = 200)
            except Master_Subscription.DoesNotExist:
                resp = Response(203,"Subscription doesnot exists")
                return JsonResponse(resp,status = 200)
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


#-------------UTILS----------------------------------------------------------------------


def get_subs_dict(subs_master):
    subs_dict = {
        'id':subs_master.id,
        'plan_name':subs_master.plan_name,
        'substype':subs_master.subscription_type,
        'is_available':subs_master.is_available
    }
    if subs_master.subscription_type == 1:
        subs_dict['no_days'] = subs_master.count_or_no_days
    else:
        subs_dict['count'] = subs_master.count_or_no_days
    return subs_dict