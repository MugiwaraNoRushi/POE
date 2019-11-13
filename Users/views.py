import json
import pyDes
import random 
from base64 import b64decode
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timezone,timedelta
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from Users.models import User_Credentials,Master_Users,Master_City,Temp_Master_Users, Master_Groups,User_Group_Mapping
from Users.utils import Response

#-------------------------------------------------------------------------------------------------

@csrf_exempt
def validate(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                keys = set(data.keys())
                if {'username','password'}.issubset(keys):
                        username = data['username']  
                        password = data['password']
                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)
                try:
                        user_obj = User_Credentials.objects.get(user_name =  username,password = password,is_active = True)
                        return get_user(request)
                except User_Credentials.DoesNotExist:
                        resp = Response(203,"Your Credentials are incorrect, Please try again")
                        return JsonResponse(resp,status = 203)
                except:
                        resp = Response(477, Exception)
                        return JsonResponse(resp,status = 477)
        else:
                resp = Response(205,'Bad Request!!')
                return JsonResponse(resp,status = 405)

#-----------------------------------------------------------------------------------------
#RANGE DO TO 6
@csrf_exempt
def signup(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                print(data)
                keys = set(data.keys())
                if {'f_name','m_name','l_name','address1','address2','email','phone','city_id','username','password','user_type'}.issubset(keys):
                        email = data['email']
                        #if email already exists !! 
                        try:
                                temp = Temp_Master_Users.objects.get(email = email)
                                now = datetime.now(timezone.utc)
                                difference = timedelta(days = 0,hours = 1,minutes = 0 )
                                if (now - temp.entry_time < difference):
                                #can also change status to show this 
                                        resp = Response(203, "Email already resgistered and check mail")
                                        return JsonResponse(resp,status = 203)
                        except Temp_Master_Users.DoesNotExist:
                                print("new email id ")
                        try:
                                temp = Master_Users.objects.get(email = email)
                                resp = Response(203, "Email already resgistered and try login ")
                                return JsonResponse(resp,status = 203)
                        except Master_Users.DoesNotExist:
                                print("new email id ")
                        city_id = data['city_id']
                        city_obj = Master_City.objects.get(id = city_id)
                        #city what to do if it does not exists
                        #user type decide 
                        random_num = int(random.randint(100000,999999))
                        user = Temp_Master_Users.objects.create(
                                username = data['username'],
                                password = data['password'],
                                first_name = data['f_name'],
                                last_name = data['l_name'],
                                middle_name = data['m_name'],
                                address1 = data['address1'],
                                address2 = data['address2'],
                                phone = data['phone'],
                                email = email,
                                user_type_id = data['user_type'],
                                city = city_obj,
                                entry_time = datetime.now(),
                                registration_code = random_num
                                )
                        user.save()
                        #what to do next
                        #call the check registration_number method !! 
                        #must make a new function 
                        val_dict = {
                                "email" : email,
                                "code":random_num
                        }
                        return JsonResponse(val_dict,status = 200)

                else:
                       resp = Response(204,"Wrong key value")
                       return JsonResponse(resp,status = 204)
                
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

#-----------------------------------------------------------------------------------------

@csrf_exempt
def validate_registration(request):
        if request.method == "POST":      
                data = json.loads(request.body.decode('utf-8'))
                #email and registration number how to fetch them !!!!
                email = data['email']
                registration_number = data['reg_num']
                #decryption remains !!
                #problem of how to fetch reg_number and email
                try:
                        user_obj = Temp_Master_Users.objects.get(email = email,registration_code = registration_number)
                        now = datetime.now(timezone.utc)
                        reg_time = user_obj.entry_time
                        #find a proper difference !! 
                        difference = timedelta(days = 0,hours = 1,minutes = 0 )
                        if (now - reg_time < difference):
                                master_user_obj = Master_Users.objects.create(
                                        first_name = user_obj.first_name,
                                        last_name = user_obj.last_name,
                                        middle_name = user_obj.middle_name,
                                        address1 = user_obj.address1,
                                        address2 = user_obj.address2,
                                        phone = user_obj.phone,
                                        email = user_obj.email,
                                        user_type_id = user_obj.user_type_id,
                                        city = user_obj.city,
                                        is_available = True
                                )
                                master_user_obj.save()
                                user_cred = User_Credentials.objects.create(
                                        user_name = user_obj.username,
                                        password = user_obj.password,
                                        user = master_user_obj
                                )  
                                user_cred.save()
                                user_obj.delete()
                                resp = Response(200,"Your account has been created successfully !")
                                return JsonResponse(resp,status = 200)
                        else:
                                resp = Response(203, "The token has expired, Please try signing up again")
                                return JsonResponse(resp,status = 203)

                except Temp_Master_Users.DoesNotExist:
                        #change the message to a proper message
                        resp = Response(203,"Wrong Registration Number !!")
                        return JsonResponse(resp,status = 203)
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

#-----------------------------------------------------------------------------------------

#how will you send the username ???
@csrf_exempt
def check_username(request):
        if request.method == "POST":
                try:
                        data = json.loads(request.body.decode('utf-8'))
                        user_cred = User_Credentials.objects.get(user_name = data['username'])
                        resp = Response(203,"Username exists and You cannot use it")
                        return JsonResponse(resp,status = 203)
                except:
                        resp = Response(200,"True")
                        return JsonResponse(resp,status = 200)
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)


#-----------------------------------------------------------------------------------------

@csrf_exempt
def change_password(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'username','old_password','new_password'}.issubset(data.keys()):
                        username = data['username']
                        old_password = data['old_password']
                        new_password = data['new_password']
                        try:
                                user_cred = User_Credentials.objects.get(user_name = username)
                                if (old_password == user_cred.password):
                                        user_cred.password = new_password
                                        user_cred.save()
                                        resp = Response(200, "password changed successfully")
                                        return JsonResponse(resp,status = 200)
                                else:
                                        resp = Response(203,"Old password is incorrect !!")
                                        return JsonResponse(resp,status = 203)
                        except User_Credentials.DoesNotExist:
                                resp = Response(203, "Wrong user name ")
                                return JsonResponse(resp,status = 203)
                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)


#----------------------------------------------------------------------------------------

@csrf_exempt
def get_user(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'username'}.issubset(data.keys()):
                        try:
                                user_obj = User_Credentials.objects.get(user_name =  data['username'])
                                user = user_obj.user
                                city = user.city
                                user_dict = {
                                        'firstName':user.first_name,
                                        'lastName' : user.last_name,
                                        'middleName':user.middle_name,
                                        'userId':user.id,
                                        'email':user.email,
                                        'phone':user.phone,
                                        'address1':user.address1,
                                        'address2':user.address2,
                                        'userTypeId':user.user_type_id,
                                        'city':{
                                        'name':city.city_text,
                                        'id' : city.id,
                                        },
                                
                                }                               
                                return JsonResponse(user_dict,status = 200)
                                
                        except User_Credentials.DoesNotExist:
                                resp = Response(203, "username doesnot exists")
                                return JsonResponse(resp,status = 203)
                
                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)


#----------------------------------------------------------------------------------------

@csrf_exempt
def create_group(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_name','user_id'}.issubset(data.keys()):
                        user_obj = Master_Users.objects.get(id = data['user_id'])
                        group_obj = Master_Groups.objects.create(group_name = data['group_name'],group_admin = user_obj)
                        group_obj.save()
                        group_dict = {
                                "name":group_obj.group_name,
                                "id":group_obj.id,
                        }
                        resp = Response(200,'Created Successfully')
                        return JsonResponse(resp,status = 200)
                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)

        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)


#-------------------------------------------------------------------------------------------------

@csrf_exempt
def add_user_to_group(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_id','user_array'}.issubset(data.keys()):
                        group_obj = Master_Groups.objects.get(id = data['group_id'])
                        user_arr = data['user_array']
                        for i in range(0,len(user_arr)):
                                user_obj = Master_Users.objects.get(id = user_arr[i])
                                group_mapping = User_Group_Mapping.objects.create(user = user_obj,group = group_obj)
                                group_mapping.save()
                        resp = Response(200,"Users added successfully")
                        return JsonResponse(resp,status = 200)

                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)


#--------------------------------------------------------------------------------------------------

#CITIES !! 

@csrf_exempt
def get_all_cities(request):
        if request.method == "POST":
                cities = Master_City.objects.all()
                arr_dict = []
                data_dict = {
                        'data':arr_dict
                }
                for city in cities:
                        temp_dict = {
                                'id':city.id,
                                'name':city.city_text,
                                'is_available':city.is_available
                        }
                        arr_dict.append(temp_dict)
                return JsonResponse(data_dict,status = 200)
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

@csrf_exempt
def delete_city(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'id'}.issubset(data.keys()):
                        try:
                                city = Master_City.objects.get(id = data['id'],is_available = True)
                                city.is_available = False
                                city.save()
                                resp = Response(200,"City deleted successfuly")
                                return JsonResponse(resp,status = 200)
                        except:
                                resp = Response(203,'city doesnot exist')
                                return JsonResponse(resp,status = 200)
                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)   
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

#activate method 1 
@csrf_exempt
def activate_city(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'id'}.issubset(data.keys()):
                        try:
                                city = Master_City.objects.get(id = data['id'],is_available = False)
                                city.is_available = True
                                city.save()
                                resp = Response(200,"City activated successfuly")
                                return JsonResponse(resp,status = 200)
                        except:
                                resp = Response(203,'city doesnot exist')
                                return JsonResponse(resp,status = 200)
                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)   
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

@csrf_exempt
def modify_city(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'id','text'}.issubset(data.keys()):
                        city = Master_City.objects.get(id = data['id'])
                        city.city_text = data['text']
                        city.save()
                        resp = Response(200,"City modified")
                        return JsonResponse(resp,status = 200)
                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)   
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

@csrf_exempt
def add_city(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'text'}.issubset(data.keys()):
                        try:
                                city = Master_City.objects.get(city_text = data['text'])
                                resp = Response(203,'City already exists ')
                                return JsonResponse(resp, status = 203)
                        except:
                                city = Master_City.objects.create(city_text = data['text'])
                                city.save()
                                resp = Response(200,"1")
                                return JsonResponse(resp,status = 200)
                else:
                        resp = Response(204,"Wrong key value")
                        return JsonResponse(resp,status = 204)   
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

@csrf_exempt
def get_all_users(request):
        if request.method == 'POST': 
                users = Master_Users.objects.all()
                arr_dict = []
                data_dict = {
                        'data':arr_dict
                }
                for user in users:
                        city = user.city
                        user_dict = {
                                'firstName':user.first_name,
                                'lastName' : user.last_name,
                                'middleName':user.middle_name,
                                'userId':user.id,
                                'email':user.email,
                                'phone':user.phone,
                                'address1':user.address1,
                                'address2':user.address2,
                                'userTypeId':user.user_type_id,
                                'city':{
                                'name':city.city_text,
                                'id' : city.id,
                                },
                        }
                        arr_dict.append(user_dict)
                return JsonResponse(data_dict,status = 200)                    
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)
