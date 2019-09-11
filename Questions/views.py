import json
from Questions.models import *
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Topics.models import Master_SubTopic

@csrf_exempt
def add_question(request):
    #choose subtopic and how to send correct option and options  
    #How to create subtopic 
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'question_type',"question_marks","question_text","difficulty","subtopic","options","correct_options"}.issubset(data.keys()):
            subtopic_obj = Master_SubTopic.objects.get(id = data['subtopic'])
            question_obj = Master_Question.objects.create(
            question_type = data['question_type'],
            question_text = data['question_text'],
            question_marks = data['question_marks'],
            difficulty = data['difficulty'],
            subtopic = subtopic_obj)
            question_obj.save()
            options_arr = data['options']
            correct_arr = data['correct_options']

            for i in range(0,len(options_arr)):
                option_obj = Master_Option.objects.create(option_text = options_arr[i],question = question_obj)
                option_obj.save()
                for j in range(0,len(correct_arr)):
                    if (i == int(correct_arr[j])):
                        correct_option = Master_Correct_Option.objects.create(option = option_obj,question = question_obj)
                        correct_option.save()

            resp = Response(200, "1")
            return JsonResponse(resp,status = 200)  
            
        else:
            resp = Response(405, "0")
            return JsonResponse(resp,status = 405)
    else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

@csrf_exempt
def delete_question(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if ({'question_id'}.issubset(data.keys())):
            question_obj = Master_Question.objects.get(id = data['question_id'])
            question_obj.is_available = False
            question_obj.save()
            option_obj = Master_Option.objects.filter(question = question_obj)
            for option in option_obj:
                option.is_available = False
                option.save()
            correct_option_obj = Master_Correct_Option.objects.filter(question = question_obj)
            for correct_option in correct_option_obj:
                correct_option.is_available = False
                correct_option.save()
            resp = Response(200,"1")
            return JsonResponse(resp,status = 200)
        else:
            resp = Response(405, "0")
            return JsonResponse(resp,status = 405)
    else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)
    
#Still not working !! 
#Complete it by tommorow 12 Sept
@csrf_exempt
def update_question(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'question_id','question_type',"question_marks","question_text","difficulty","subtopic","options","correct_options"}.issubset(data.keys()):
            subtopic_obj = Master_SubTopic.objects.get(id = data['subtopic'])
            question_obj = Master_Question.objects.get(id = data['question_id'])
            question_obj.question_type = data['question_type']
            question_obj.question_text = data['question_text']
            question_obj.question_marks = data['question_marks']
            question_obj.difficulty = data['difficulty']
            question_obj.subtopic = subtopic_obj
            question_obj.save()
            options_arr = data['options']
            correct_arr = data['correct_options']
            resp = Response(200, "1")
            return JsonResponse(resp,status = 200)  
        else:
            resp = Response(405, "0")
            return JsonResponse(resp,status = 405)
    else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)


