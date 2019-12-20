#question assigned and question response

import json
import random 
from Exams.models import *
from Users.models import *
from Template.models import *
from Questions.models import *
from Questions.views import *
from django.http import JsonResponse
from Users.utils import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from POE.authentication import authenticate

@csrf_exempt
def assign_questions_to_exam(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'user_id','exam_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            template_section_arr_obj = []
            #get a template by using exam_id
            try:
                exam_obj = Master_Exam.objects.get(id = data['exam_id'],is_available = True)
                user_obj = Master_Users.objects.get(id = data['user_id'],is_available = True)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Users.DoesNotExist:
                resp = Response(203,'User doesnot exists')
                return JsonResponse(resp,status = 203)

            #CHECKING if question is already assigned
            try:
                user_question_assigned_arr = User_Question_Assigned.objects.filter(exam = exam_obj,user = user_obj)
                if len(user_question_assigned_arr) > 0:
                    question = user_question_assigned_arr[0].question
                    print(question)
                    return JsonResponse(soul(question,user_question_assigned_arr),status = 200)
            except User_Question_Assigned.DoesNotExist:
                print('called')
            except Exception as e:
                resp = Response(203,'Something went wrong')
                return JsonResponse(resp,status = 203)
            #fetch sections based on template
            try:
                template_obj = exam_obj.template
                section_arr_obj = Master_Section.objects.filter(template = template_obj,is_available = True)
            except:
                print('in try block 2 error is with filter of Master sections')
                resp = Response(203,'Master Section error persists')
                return JsonResponse(resp,status = 203)

            #fetch all template sections based on sections
            try:
                for section_obj in section_arr_obj:
                    temp_temp_section_arr = Template_Section.objects.filter(section =section_obj,is_available = True)
                    for temp_section in temp_temp_section_arr:
                        template_section_arr_obj.append(temp_section)
            except:
                print('in try block 3 error is with template_Section or with appending the objects')
                resp = Response(203,'Template Section error persists')
                return JsonResponse(resp,status = 203)

            try:
                for temp_section_obj in template_section_arr_obj:
                    subtopic_obj = temp_section_obj.subtopic
                    section_obj = temp_section_obj.section
                    questions = Master_Question.objects.filter(subtopic = subtopic_obj,is_available = True)
                    questions = list(questions)
                    for i in range(0,temp_section_obj.no_questions):
                        rand_index = random.randint(0,len(questions)-1)
                        question = questions[rand_index]
                        user_question_assigned_obj = User_Question_Assigned.objects.create(
                            question = question,
                            exam = exam_obj,
                            user = user_obj,
                            section = section_obj
                        )
                        user_question_assigned_obj.save()
                        user_question_response_obj = User_Question_Response.objects.create(
                            section_question = user_question_assigned_obj,
                            option = None
                        )
                        user_question_response_obj.save()
                        questions.remove(question)
                        print(i)
                        print(question)
                    
            except Exception as e:
                print(e)
                resp = Response(203,'Question Subtopic error persists')
                return JsonResponse(resp,status = 203)
            #FINAL RESULT TO SEND
            user_question_assigned_arr = User_Question_Assigned.objects.filter(exam = exam_obj,user = user_obj)
            question = user_question_assigned_arr[0].question
            return JsonResponse(soul(question,user_question_assigned_arr),status = 200)
        
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)




#new method
@csrf_exempt
def scroll_through_exam(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'question_assigned_id','option_id','marked','next_question_id','user_id','exam_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                #response saved
                user_response = User_Question_Response.objects.get(section_question = data['question_assigned_id'])
                option_obj = Master_Option.objects.get(id = data['option_id'])
                user_response.option = option_obj
                user_response.marked = data['marked']
                user_response.save()
                #question fetched
                question = Master_Question.objects.get(id = data['next_question_id'])
                #will use that question in calling soul
            except User_Question_Response.DoesNotExist:
                resp = Response(203,'Response doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Question.DoesNotExist:
                resp = Response(203,'Wrong Next Question id and it doesnot exists')
                return JsonResponse(resp,status = 203)
            
            #fetch exam and user
            try:
                exam_obj = Master_Exam.objects.get(id = data['exam_id'])
                user_obj = Master_Users.objects.get(id = data['user_id'])
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Users.DoesNotExist:
                resp = Response(203,'User doesnot exists')
                return JsonResponse(resp,status = 203)

            user_question_assigned_arr = User_Question_Assigned.objects.filter(exam = exam_obj,user = user_obj)
            return JsonResponse(soul(question,user_question_assigned_arr),status = 200)

       
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)




@csrf_exempt
def get_result(request):
    if request.method == 'POST':
        data =json.loads(request.body.decode('utf-8'))
        if {'user_id','exam_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
            try:
                exam_obj = Master_Exam.objects.get(id = data['exam_id'])
                user_obj = Master_Users.objects.get(id = data['user_id'])
                exam_status = User_Test_Status.objects.get(user = user_obj,exam = exam_obj)
                if exam_status.status != 3:
                    resp = Response(203,'Exam has not been completed yet')
                    return JsonResponse(resp,status = 200)
                user_question_assigned_arr = User_Question_Assigned.objects.filter(exam = exam_obj,user = user_obj)
            except User_Test_Status.DoesNotExist:
                resp = Response(203,'User_Test_Status doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Exam.DoesNotExist:
                resp = Response(203,'Exam doesnot exists')
                return JsonResponse(resp,status = 203)
            except Master_Users.DoesNotExist:
                resp = Response(203,'User doesnot exists')
                return JsonResponse(resp,status = 203)  
            except User_Question_Assigned.DoesNotExist:
                resp = Response(203,'User has not been assigned questions')
                return JsonResponse(resp,status = 203) 
            template = exam_obj.template


            total_marks = template.template_marks
            marks_obtained = 0
            for user_question_assigned in user_question_assigned_arr:
                try:
                    user_response_arr = User_Question_Response.objects.filter(section_question = user_question_assigned)
                    question_assigned = user_question_assigned.question
                    negative_marks = user_question_assigned.section.negative_marks
                    correct_options_set = {}
                    correct_options = Master_Correct_Option.objects.filter(question = question_assigned)
                    for correct_option in correct_options:
                        correct_options_set.add(correct_option.option)

                    attempted_options_set = {}
                    for user_response in user_response_arr:
                        attempted_options_set.add(user_response.option)

                    if attempted_options_set == correct_options_set:
                        marks_obtained = marks_obtained + (question_assigned.question_marks * question_assigned.difficulty)                        
                    else:
                        marks_obtained = marks_obtained - negative_marks


                except User_Question_Response.DoesNotExist:
                    pass
        
        marks_dict = {
            'marks_obtained':marks_obtained,
            'total_marks':total_marks
        }   
        return JsonResponse(marks_dict,status = 200)         
         
    resp = Response(405,'Bad Request!!')
    return JsonResponse(resp,status = 405)     


    #a new model would be better ????


    
#-------------------UTILS METHODS ---------------------------------------------------




def soul(question_to_be_fetched,user_question_assigned_arr):
    user_question_response_arr = []

    for user_question_assigned_obj in user_question_assigned_arr:
        user_response = User_Question_Response.objects.get(section_question = user_question_assigned_obj)
        user_question_response_arr.append(user_response)
    
    main_arr = []
    main_dict = {
        "data":main_arr
    }
    for i in range(0,len(user_question_assigned_arr)):
        question = user_question_assigned_arr[i].question
        temp_obj = {
            'question_id':question.id,
            'marked':user_question_response_arr[i].marked,
            'user_question_assigned_id':user_question_assigned_arr[i].id
        }
        if user_question_response_arr[i].option == None:
            temp_obj['response'] = False
        else:
            temp_obj['response'] = True
        main_arr.append(temp_obj)
    main_dict['first_question'] = get_single_question(question_to_be_fetched)
    print('here')
    return main_dict



