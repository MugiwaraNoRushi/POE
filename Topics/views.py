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
                resp = Response(203,"Topic already exists")
                return JsonResponse(resp, status = 203)
            except Master_Topic.DoesNotExist:
                topic = Master_Topic.objects.create(topic_text = data['text'])
                topic.save()
                resp = Response(200,"Created successfully")
                return JsonResponse(resp,status = 200)
        else:
            resp = Response(204, "Wrong key value ")
            return JsonResponse(resp,status = 204)
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
                resp = Response(203,"SubTopic already exists")
                return JsonResponse(resp, status = 203)
            except Master_SubTopic.DoesNotExist:
                subtopic = Master_SubTopic.objects.create(subtopic_text = data['text'],topic = topic)
                subtopic.save()
                resp = Response(200,"Created successfully")
                return JsonResponse(resp,status = 200)
        else:
            resp = Response(204, "Wrong key value")
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def get_all_topics(request):
    if request.method == 'POST':
        topics_arr = []
        topics_dict = {'data':topics_arr}
        topics = Master_Topic.objects.all()
        for topic in topics:
            temp = {
                'id':topic.id,
                'text':topic.topic_text,
            }
            topics_arr.append(temp)
        return JsonResponse(topics_dict,status = 200)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def get_all_subtopics(request):
    if request.method == 'POST':
        subtopics_arr = []
        subtopics_dict = {'data':subtopics_arr}
        subtopics = Master_SubTopic.objects.all()
        for subtopic in subtopics:
            temp = {
                'id':subtopic.id,
                'text':subtopic.subtopic_text,
            }
            subtopics_arr.append(temp)
        return JsonResponse(subtopics_dict,status = 200)
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
                subtopic = Master_SubTopic.objects.get(id = data['id'],is_available = True)
                subtopic.is_available = False
                subtopic.save()
                resp = Response(200, "Deleted successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"Subtopic doesnot exist")
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204, "Wrong key value")
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_topic(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if {'id'}.issubset(data.keys()):
            try:
                topic = Master_Topic.objects.get(id = data['id'],is_available = True)
                topic.is_available = False
                topic.save()
                resp = Response(200, "Deleted successfully")
                return JsonResponse(resp, status = 200)
            except Master_SubTopic.DoesNotExist:
                resp = Response(203,"topic doesnot exist")
                return JsonResponse(resp,status = 203)
        else:
            resp = Response(204, "Wrong key value")
            return JsonResponse(resp,status = 204)
    else:
        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

#update topic and suptopic 
#get single subtopic id and topic id 
#get all subtopics ==>> include topic object