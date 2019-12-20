import json
from Questions.models import *
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Topics.models import Master_SubTopic

@csrf_exempt
def add_questions(request):
    print('first stage')
    print('subtopic 1')
    try:
        options_arr = ['option_a','option_b','option_c','option_d']
        correct_arr = [0]
        subtopic_1 = Master_SubTopic.objects.get(id = 3)
        subtopic_2 = Master_SubTopic.objects.get(id = 4)
        subtopic_3 = Master_SubTopic.objects.get(id = 5)
    except:
        print('in try 1 maybe a subtopic error ')
        resp = Response(204, "Wrong key value pair in try part 0")
        return JsonResponse(resp,status  = 200)


    try:
        for i in range(33):
            question_obj = Master_Question.objects.create(
                question_text = 'question' + str(i),
                question_marks = 1,
                difficulty = 1,
                question_type = 1,
                subtopic = subtopic_1
            )
            question_obj.save()
            for i in range(0,len(options_arr)):
                option_obj = Master_Option.objects.create(option_text = options_arr[i],question = question_obj)
                option_obj.save()
                for j in range(0,len(correct_arr)):
                    if (i == int(correct_arr[j])):
                        correct_option = Master_Correct_Option.objects.create(option = option_obj,question = question_obj)
                        correct_option.save()

    except Exception as e:
        print('error in for looop 1')
        print(e)
        resp = Response(204, "Wrong key value pair in try part 1")
        return JsonResponse(resp,status  = 200)


    try:
        for i in range(33):
            question_obj = Master_Question.objects.create(
                question_text = 'question' + str(i + 33),
                question_marks = 1,
                difficulty = 1,
                question_type = 1,
                subtopic = subtopic_2
            )
            question_obj.save()
            for i in range(0,len(options_arr)):
                option_obj = Master_Option.objects.create(option_text = options_arr[i],question = question_obj)
                option_obj.save()
                for j in range(0,len(correct_arr)):
                    if (i == int(correct_arr[j])):
                        correct_option = Master_Correct_Option.objects.create(option = option_obj,question = question_obj)
                        correct_option.save()
    except:
        print('error in for loop 2')
        resp = Response(204, "Wrong key value pair in try part 2")
        return JsonResponse(resp,status  = 200)


    try:
        for i in range(33):
            question_obj = Master_Question.objects.create(
                question_text = 'question' + str(i + 66),
                question_marks = 1,
                difficulty = 1,
                question_type = 1,
                subtopic = subtopic_3
            )
            question_obj.save()
            for i in range(0,len(options_arr)):
                option_obj = Master_Option.objects.create(option_text = options_arr[i],question = question_obj)
                option_obj.save()
                for j in range(0,len(correct_arr)):
                    if (i == int(correct_arr[j])):
                        correct_option = Master_Correct_Option.objects.create(option = option_obj,question = question_obj)
                        correct_option.save()
    except:
        print('error in for loop 3')
        resp = Response(204, "Wrong key value pair in try part 3")
        return JsonResponse(resp,status  = 200)

    resp = Response(200, "Questionssss added successfully")
    return JsonResponse(resp,status = 200)  