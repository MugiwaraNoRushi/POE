import json
from Topics.models import *
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

#decide about what to do with creation of multiple same topics
@csrf_exempt
def create_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'text'}.issubset(data.keys()):
            try:
                topic = Master_Topic.objects.get(topic_text = data['text'])
                resp = Response(405,"Topic already exists")
                return JsonResponse(resp, status = 405)
            except Master_Topic.DoesNotExist:
                topic = Master_Topic.objects.create(topic_text = data['text'])
                topic.save()
                resp = Response(200,"Created successfully")
                return JsonResponse(resp,status = 200)
        else:
            resp = Response(405, "Wrong key value ")
            return JsonResponse(resp,status = 405)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def create_subtopic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'text','topic_id'}.issubset(data.keys()):
            try:
                topic = Master_Topic.objects.get(id = data['topic_id'])
                subtopic = Master_SubTopic.objects.get(subtopic_text = data['text'],topic = data['topic_id'])
                resp = Response(405,"SubTopic already exists")
                return JsonResponse(resp, status = 405)
            except Master_SubTopic.DoesNotExist:
                subtopic = Master_SubTopic.objects.create(subtopic_text = data['text'],topic = topic)
                subtopic.save()
                resp = Response(200,"Created successfully")
                return JsonResponse(resp,status = 200)
        else:
            resp = Response(405, "Wrong key value")
            return JsonResponse(resp,status = 405)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def get_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'text'}.issubset(data.keys()):
            try:
                topic = Master_Topic.objects.get(topic_text = data['text'],is_available = True)
                topic_dict = {
                    "topic_text":topic.topic_text,
                    "topic_id":topic.id
                }
                return JsonResponse(topic_dict, status = 200)
            except Master_Topic.DoesNotExist:
                resp = Response(405,"Topic doesnot exist")
                return JsonResponse(resp,status = 405)
        else:
            resp = Response(405, "Wrong key value ")
            return JsonResponse(resp,status = 405)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def get_subtopic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'text','topic_id'}.issubset(data.keys()):
            try:
                topic = Master_Topic.objects.get(id = data['topic_id'])
                subtopic = Master_SubTopic.objects.get(subtopic_text = data['text'],topic = data['topic_id'],is_available = True)
                subtopic_dict = {
                    "subtopic_text":subtopic.subtopic_text,
                    "subtopic_id":subtopic.id,
                    "topic":{
                        "id":topic.id,
                        "topic_text":topic.topic_text
                    }
                }
                return JsonResponse(subtopic_dict, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(405,"Subtopic doesnot exist")
                return JsonResponse(resp,status = 405)
        else:
            resp = Response(405, "Wrong key value")
            return JsonResponse(resp,status = 405)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

#-------------------------------------------------------------------------------------------


@csrf_exempt
def delete_subtopic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:
                subtopic = Master_SubTopic.objects.get(id = data['id'])
                subtopic.is_avaible = False
                subtopic.save()
                resp = Response(200, "Deleted successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(405,"Subtopic doesnot exist")
                return JsonResponse(resp,status = 405)
        else:
            resp = Response(405, "Wrong key value")
            return JsonResponse(resp,status = 405)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:
                topic = Master_Topic.objects.get(id = data['id'])
                topic.is_avaible = False
                topic.save()
                resp = Response(200, "Deleted successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(405,"topic doesnot exist")
                return JsonResponse(resp,status = 405)
        else:
            resp = Response(405, "Wrong key value")
            return JsonResponse(resp,status = 405)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)
