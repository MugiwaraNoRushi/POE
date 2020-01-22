import json
from Topics.models import *
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from POE.authentication import authenticate

#decide about what to do with creation of multiple same topics
@csrf_exempt
def create_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'text','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                topic = Master_Topic.objects.get(topic_text = data['text'])
                resp = Response(203,"Topic already exists")
                return JsonResponse(resp, status  = 200)
            except Master_Topic.DoesNotExist:
                topic = Master_Topic.objects.create(topic_text = data['text'])
                topic.save()
                resp = Response(200,"Created successfully")
                return JsonResponse(resp,status = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def create_subtopic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'text','topic_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                topic = Master_Topic.objects.get(id = data['topic_id'])
                subtopic = Master_SubTopic.objects.get(subtopic_text = data['text'],topic = data['topic_id'])
                resp = Response(203,"SubTopic already exists")
                return JsonResponse(resp, status  = 200)
            except Master_SubTopic.DoesNotExist:
                subtopic = Master_SubTopic.objects.create(subtopic_text = data['text'],topic = topic)
                subtopic.save()
                resp = Response(200,"Created successfully")
                return JsonResponse(resp,status = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def get_all_topics(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            topics_arr = []
            topics_dict = {'data':topics_arr}
            topics = Master_Topic.objects.all()
            for topic in topics:
                temp = {
                    'id':topic.id,
                    'text':topic.topic_text,
                    'is_available':topic.is_available
                }
                topics_arr.append(temp)
            return JsonResponse(topics_dict,status = 200)

    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def get_all_subtopics(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            subtopics_arr = []
            subtopics_dict = {'data':subtopics_arr}
            subtopics = Master_SubTopic.objects.all()
            for subtopic in subtopics:
                topic = subtopic.topic
                temp = {
                    'id':subtopic.id,
                    'text':subtopic.subtopic_text,
                    'is_available':subtopic.is_available,
                    'topic':{
                        'id':topic.id,
                        'text':topic.topic_text,
                        'is_available':topic.is_available
                    }
                }
                subtopics_arr.append(temp)
            return JsonResponse(subtopics_dict,status = 200)

    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

#-------------------------------------------------------------------------------------------


@csrf_exempt
def delete_subtopic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                subtopic = Master_SubTopic.objects.get(id = data['id'],is_available = True)
                subtopic.is_available = False
                subtopic.save()
                resp = Response(200, "Deleted successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"Subtopic doesnot exist")
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                topic = Master_Topic.objects.get(id = data['id'],is_available = True)
                topic.is_available = False
                topic.save()
                resp = Response(200, "Deleted successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"topic doesnot exist")
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def update_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','text','auth_key'}.issubset(data.keys())  and authenticate(data['auth_key']):
            try:
                topic = Master_Topic.objects.get(id = data['id'],is_available = True)
                topic.topic_text = data['text']
                topic.save()
                resp = Response(200, "Updated successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"topic doesnot exist")
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def update_subtopic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','id','text','topic_id'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                topic = Master_Topic.objects.get(id = data['topic_id'])
                subtopic = Master_SubTopic.objects.get(id = data['id'])
                subtopic.subtopic_text = data['text']
                subtopic.topic = topic
                subtopic.save()
                resp = Response(200, "Updated successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"Subtopic doesnot exist")
                return JsonResponse(resp,status  = 200)
            except Master_Topic.DoesNotExist:
                resp = Response(203,"topic doesnot exist")
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def get_subtopic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys())  and authenticate(data['auth_key']):
            try:
                subtopic = Master_SubTopic.objects.get(id = data['id'],is_available = True)
                topic = subtopic.topic
                subtopic_dict = {
                    'id':subtopic.id,
                    'text':subtopic.subtopic_text,
                    'is_available':subtopic.is_available,
                    'topic':{
                        'id':topic.id,
                        'text':topic.topic_text,
                        'is_available':topic.is_available
                    }
                }
                return JsonResponse(subtopic_dict,status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"Subtopic doesnot exist")
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def get_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys())  and authenticate(data['auth_key']):
            try:
                topic = Master_Topic.objects.get(id = data['id'])
                topic_dict = {
                    'id':topic.id,
                    'text':topic.topic_text,
                    'is_available':topic.is_available
                }
                return JsonResponse(topic_dict,status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"topic doesnot exist")
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)



#update topic and suptopic
#get single subtopic id and topic id
#get all subtopics ==>> include topic object


@csrf_exempt
def activate_subtopic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                subtopic = Master_SubTopic.objects.get(id = data['id'],is_available = False)
                subtopic.is_available = True
                subtopic.save()
                resp = Response(200, "Activated successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"Subtopic doesnot exist")
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def activate_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                topic = Master_Topic.objects.get(id = data['id'],is_available = False)
                topic.is_available = True
                topic.save()
                resp = Response(200, "Activated successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"topic doesnot exist")
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

#

@csrf_exempt
def delete_topic_perman(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                topic = Master_Topic.objects.get(id = data['id'],is_available = True)
                topic.delete()
                resp = Response(200, "Deleted permanently")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"topic doesnot exist")
                return JsonResponse(resp,status  = 200)
    
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_subtopic_perman(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                subtopic = Master_SubTopic.objects.get(id = data['id'],is_available = True)
                subtopic.delete()
                resp = Response(200, "Deleted permanently")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"Subtopic doesnot exist")
                return JsonResponse(resp,status  = 200)
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)
