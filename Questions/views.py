import json
from Questions.models import *
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Topics.models import Master_SubTopic
from POE.authentication import *

@csrf_exempt
def add_question(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','question_type',"question_marks","question_text","difficulty","subtopic","options","correct_options"}.issubset(data.keys()) and authenticate(data['auth_key']):
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

            resp = Response(200, "Question added successfully")
            return JsonResponse(resp,status = 200)  
            
       
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)

@csrf_exempt
def delete_question(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if ({'question_id','auth_key'}.issubset(data.keys())) and authenticate(data['auth_key']):
            try:
                question_obj = Master_Question.objects.get(id = data['question_id'],is_available = True)
                question_obj.is_available = False
                question_obj.save()
                option_obj = Master_Option.objects.filter(question = question_obj,is_available =True)
                for option in option_obj:
                    option.is_available = False
                    option.save()
                correct_option_obj = Master_Correct_Option.objects.filter(question = question_obj,is_available = True)
                for correct_option in correct_option_obj:
                    correct_option.is_available = False
                    correct_option.save()
                resp = Response(200,"Question deleted successfully")
                return JsonResponse(resp,status = 200)
            except:
                resp = Response(203,'Question or Options doesnot exists')
                return JsonResponse(resp,status = 203)
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)
    
@csrf_exempt
def update_question(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'auth_key','question_id','question_type',"question_marks","question_text","difficulty","subtopic","options","correct_options"}.issubset(data.keys()) and authenticate(data['auth_key']):
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
            correct_objs = Master_Correct_Option.objects.filter(question = int(data['question_id']))
            print(correct_objs)
            #deleting past correct options
            for correct_obj in correct_objs:
                correct_obj.is_available = False
                correct_obj.save()
            #deleting past options
            option_objs = Master_Option.objects.filter(question = int(data['question_id']))
            for option_obj in option_objs:
                option_obj.is_available = False
                option_obj.save()
            for i in range(0,len(options_arr)):
                option_obj = Master_Option.objects.create(option_text = options_arr[i],question = question_obj)
                option_obj.save()
                for j in range(0,len(correct_arr)):
                    if (i == int(correct_arr[j])):
                        correct_option = Master_Correct_Option.objects.create(option = option_obj,question = question_obj)
                        correct_option.save()    
            resp = Response(200, "Question modified successfully")
            return JsonResponse(resp,status = 200)  
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)



@csrf_exempt
def get_all_questions(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if {'subtopic_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            subtopic = Master_SubTopic.objects.get(id = data['subtopic_id'])
            questions = Master_Question.objects.filter(subtopic = subtopic,is_available = True)
            arr_dict = []
            questions_data = {'data':arr_dict}
            try:
                for question in questions:
                    arr_dict.append(get_single_question(question))
                return JsonResponse(questions_data,status = 200)
            except:
                resp = Response('Something went wrong GEN 1',Exception)
                return JsonResponse(resp, status = 477)
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)


#-----------------UTILS----------------------------------------------------------------------------


#get single question
def get_single_question(question):
    option_arr = []
    correct_option_arr = []
    options = Master_Option.objects.filter(question = question,is_available = True)
    for option in options:
        option_dict = {
            'option_text':option.option_text,
            'option_id':option.id
        }
        option_arr.append(option_dict)
    correct_options = Master_Correct_Option.objects.filter(question = question,is_available = True)
    for correct_option in correct_options:
        correct_option_dict = {
            'correct_option_text':str(correct_option.option.option_text),
            'correct_option_id':correct_option.id
        }
        correct_option_arr.append(correct_option_dict)
    question_dict = {
        'question_text':question.question_text,
        'question_marks':question.question_marks,
        'question_id':question.id,
        'question_type':question.question_type,
        'question_difficulty':question.difficulty,
        'options':option_arr,
        'correct_options':correct_option_arr
    }
    return question_dict