import json
import random,string
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timezone,timedelta
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from Users.models import User_Credentials,Master_Users,Master_City,Temp_Master_Users, Master_Groups,User_Group_Mapping
from Users.utils import *
from POE.authentication import authenticate

#-------------------------------------------------------------------------------------------------

@csrf_exempt
def validate(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                keys = set(data.keys())
                if {'username','password','auth_key'}.issubset(keys) and authenticate(data['auth_key']):
                        username = data['username']
                        password = data['password']
                else:
                        resp = Response(401,"Bad Request")
                        return JsonResponse(resp,status  = 200)
                try:
                        user_obj = User_Credentials.objects.get(user_name =  username,password = password,is_active = True)
                        return get_user(request)
                except User_Credentials.DoesNotExist:
                        resp = Response(203,"Your Credentials are incorrect, Please try again")
                        return JsonResponse(resp,status  = 200)
                except:
                        resp = Response(477, Exception)
                        return JsonResponse(resp,status = 477)
        else:
                resp = Response(405,'Bad Request!!')
                return JsonResponse(resp,status = 405)

#-----------------------------------------------------------------------------------------
#RANGE DO TO 6
@csrf_exempt
def signup(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                keys = set(data.keys())
                if {'auth_key','f_name','m_name','l_name','address1','address2','email','phone','city_id','username','password','user_type'}.issubset(keys) and authenticate(data['auth_key']):
                        email = data['email']
                        #if email already exists !!
                        try:
                                temp = Temp_Master_Users.objects.get(email = email)
                                now = datetime.now(timezone.utc)
                                difference = timedelta(days = 0,hours = 1,minutes = 0 )
                                if (now - temp.entry_time < difference):
                                #can also change status to show this
                                        resp = Response(203, "Email already resgistered and check mail")
                                        return JsonResponse(resp,status  = 200)
                        except Temp_Master_Users.DoesNotExist:
                                print("new email id ")
                        try:
                                temp = Master_Users.objects.get(email = email)
                                resp = Response(203, "Email already resgistered and try login ")
                                return JsonResponse(resp,status  = 200)
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
                        sendEmail_reg_code(data['username'],random_num,email)
                        user.save()
                        val_dict = {
                                "email" : email,
                                "code":0
                        }
                        return JsonResponse(val_dict,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

#-----------------------------------------------------------------------------------------

@csrf_exempt
def validate_registration(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','email','reg_num'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        email = data['email']
                        registration_number = data['reg_num']
                        try:
                                user_obj = Temp_Master_Users.objects.get(email = email,registration_code = registration_number)
                                now = datetime.now(timezone.utc)
                                reg_time = user_obj.entry_time
                                difference = timedelta(days = 0,hours = 1,minutes = 0 )
                                if (now - reg_time < difference):
                                        if user_obj.user_type_id == 3:
                                                #in case of student
                                                active = True
                                        elif user_obj.user_type_id == 2:
                                                active = False
                                                sendEmail_faculty(user_obj.username,user_obj.email)
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
                                                is_available = active,
                                        )
                                        master_user_obj.save()
                                        user_cred = User_Credentials.objects.create(
                                                user_name = user_obj.username,
                                                password = user_obj.password,
                                                user = master_user_obj,
                                                is_active = active
                                        )
                                        user_cred.save()
                                        user_obj.delete()
                                        resp = Response(200,"Your account has been created successfully !")
                                        return JsonResponse(resp,status = 200)
                                else:
                                        resp = Response(203, "The token has expired, Please try signing up again")
                                        return JsonResponse(resp,status  = 200)

                        except Temp_Master_Users.DoesNotExist:
                                #change the message to a proper message
                                resp = Response(203,"Wrong Registration Number !!")
                                return JsonResponse(resp,status  = 200)
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
                        #check for temp data base 
                        resp = Response(203,"Username exists and You cannot use it")
                        return JsonResponse(resp,status  = 200)
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
                if {'auth_key','user_id','old_password','new_password'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        user_id = data['user_id']
                        old_password = data['old_password']
                        new_password = data['new_password']
                        try:
                                user_obj = Master_Users.objects.get(id = user_id)
                                user_cred = User_Credentials.objects.get(user = user_obj)
                                if (old_password == user_cred.password):
                                        user_cred.password = new_password
                                        user_cred.save()
                                        resp = Response(200, "password changed successfully")
                                        return JsonResponse(resp,status = 200)
                                else:
                                        resp = Response(203,"Current password is incorrect !!")
                                        return JsonResponse(resp,status  = 200)
                        except User_Credentials.DoesNotExist:
                                resp = Response(203, "Wrong user name ")
                                return JsonResponse(resp,status  = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


#----------------------------------------------------------------------------------------

@csrf_exempt
def get_user_by_id(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','user_id'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                user_obj = User_Credentials.objects.get(id = data['user_id'])
                                user = user_obj.user
                                return JsonResponse(get_user_dict(user),status = 200)

                        except User_Credentials.DoesNotExist:
                                resp = Response(203, "user doesnot exists")
                                return JsonResponse(resp,status  = 200)


        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def get_user(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','username'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                user_obj = User_Credentials.objects.get(user_name =  data['username'])
                                user = user_obj.user
                                resp = Response(200,get_user_dict(user))
                                return JsonResponse(resp,status = 200)

                        except User_Credentials.DoesNotExist:
                                resp = Response(203, "username doesnot exists")
                                return JsonResponse(resp,status  = 200)


        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def get_all_users(request):
        if request.method == 'POST':
                data =json.loads(request.body.decode('utf-8'))
                if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        users = Master_Users.objects.all()
                        arr_dict = []
                        data_dict = {
                                'data':arr_dict
                        }
                        for user in users:
                                arr_dict.append(get_user_dict(user))
                        return JsonResponse(data_dict,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def delete_user(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'user_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                user_obj = Master_Users.objects.get(id = data['user_id'])
                                user_cred_obj = User_Credentials.objects.get(user = user_obj)
                        except:
                                resp = Response(203,'User does not exists')
                                return JsonResponse(resp,status  = 200)

                        user_obj.is_available = False
                        user_obj.save()

                        user_cred_obj.is_active = False
                        user_cred_obj.save()

                        resp = Response(200,'User deleted successfully ')
                        return JsonResponse(resp,status = 200)


        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def activate_user(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'user_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                user_obj = Master_Users.objects.get(id = data['user_id'])
                                user_cred_obj = User_Credentials.objects.get(user = user_obj)
                        except:
                                resp = Response(203,'User does not exists')
                                return JsonResponse(resp,status  = 200)

                        user_obj.is_available = True
                        user_obj.save()

                        user_cred_obj.is_active = True
                        user_cred_obj.save()

                        resp = Response(200,'User activated successfully ')
                        return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

#----------------------------------------------------------------------------------------

#GROUPS

@csrf_exempt
def create_group(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','group_name','user_id'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        user_obj = Master_Users.objects.get(id = data['user_id'])
                        group_obj = Master_Groups.objects.create(group_name = data['group_name'],group_admin = user_obj)
                        group_obj.save()
                        group_dict = {
                                "name":group_obj.group_name,
                                "id":group_obj.id,
                        }
                        resp = Response(200,'Created Successfully')
                        return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


#-------------------------------------------------------------------------------------------------


@csrf_exempt
def get_group(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','group_id'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                group = Master_Groups.objects.get(id = data['group_id'])
                                return JsonResponse(get_group_dict(group), status = 200)
                        except:
                                resp = Response(203,'Group doesnot exists')
                                return JsonResponse(resp,status  = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

#Changes remain from here


@csrf_exempt
def get_all_groups(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        groups = Master_Groups.objects.all()
                        arr_dict = []
                        data_dict = {
                                'data':arr_dict
                        }
                        for group in groups:
                                arr_dict.append(get_group_dict(group))
                        return JsonResponse(data_dict,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def add_user_to_group(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_id','user_array','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        print(data['user_array'])
                        try:
                                group_obj = Master_Groups.objects.get(id = data['group_id'],is_available = True)
                        except:
                                resp = Response(203,'Group doesnot exists')
                                return JsonResponse(resp,status  = 200)
                        user_arr = data['user_array']
                        for i in range(0,len(user_arr)):
                                user_obj = Master_Users.objects.get(id = user_arr[i])
                                group_mapping = User_Group_Mapping.objects.create(user = user_obj,group = group_obj)
                                group_mapping.save()
                        resp = Response(200,"Users added successfully")
                        return JsonResponse(resp,status = 200)


        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def remove_user_from_group(request):

        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_id','user_array','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                group_obj = Master_Groups.objects.get(id = data['group_id'],is_available = True)
                        except:
                                resp = Response(203,'Group doesnot exists')
                                return JsonResponse(resp,status  = 200)

                        user_arr = data['user_array']
                        for i in range(0,len(user_arr)):
                                user_obj = Master_Users.objects.get(id = user_arr[i],is_available = True)
                                group_mapping = User_Group_Mapping.objects.get(user = user_obj,group = group_obj)
                                group_mapping.delete()
                        resp = Response(200,"Users deleted successfully")
                        return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def get_users_from_group(request):

        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                group_obj = Master_Groups.objects.get(id = data['group_id'])
                                user_group_mappings = User_Group_Mapping.objects.filter(group = group_obj)

                        except:
                                resp = Response(203,'Group doesnot exists')
                                return JsonResponse(resp,status  = 200)

                        arr_dict = []
                        data_dict = {
                            'data':arr_dict
                        }
                        for i in range(0,len(user_group_mappings)):
                                user_obj = user_group_mappings[i].user
                                arr_dict.append(get_user_dict(user_obj))

                        return JsonResponse(data_dict,status = 200)


        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def get_groups_from_user(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'user_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                            user_obj = Master_Users.objects.get(id = data['user_id'])
                            user_group_mappings = User_Group_Mapping.objects.filter(user = user_obj)

                        except:
                                resp = Response(203,'Groups do not exists')
                                return JsonResponse(resp,status  = 200)

                        arr_dict = []
                        data_dict = {
                            'data':arr_dict
                        }
                        for i in range(0,len(user_group_mappings)):
                                group_obj = user_group_mappings[i].group
                                arr_dict.append(get_group_dict(group_obj))

                        return JsonResponse(data_dict,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def modify_group(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_id','group_name','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                group_obj = Master_Groups.objects.get(id = data['group_id'])
                        except:
                                resp = Response(203,'Group does not exists')
                                return JsonResponse(resp,status  = 200)

                        group_obj.group_name = data['group_name']
                        group_obj.save()
                        resp = Response(200,'Group modified successfully ')
                        return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_group(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                group_obj = Master_Groups.objects.get(id = data['group_id'],is_available = True)
                        except:
                                resp = Response(203,'Group doesnot exists')
                                return JsonResponse(resp,status  = 200)

                        group_obj.is_available = False
                        group_obj.save()
                        resp = Response(200,'Group deleted successfully ')
                        return JsonResponse(resp,200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def activate_group(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                group_obj = Master_Groups.objects.get(id = data['group_id'],is_available = False)
                        except:
                                resp = Response(203,'Group doesnot exists')
                                return JsonResponse(resp,status  = 200)

                        group_obj.is_available = True
                        group_obj.save()
                        resp = Response(200,'Group activated successfully ')
                        return JsonResponse(resp,200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


#--------------------------------------------------------------------------------------------------

#CITIES !!

@csrf_exempt
def get_city(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        city = Master_City.objects.get(id = data['id'])
                        arr_dict = []
                        city_dict = {
                                'id':city.id,
                                'name':city.city_text,
                                'is_available':city.is_available
                        }

                        return JsonResponse(city_dict,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def get_all_cities(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
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

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def delete_city(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                city = Master_City.objects.get(id = data['id'],is_available = True)
                                city.is_available = False
                                city.save()
                                resp = Response(200,"City deleted successfuly")
                                return JsonResponse(resp,status = 200)
                        except:
                                resp = Response(203,'city doesnot exist')
                                return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

#activate method 1
@csrf_exempt
def activate_city(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                city = Master_City.objects.get(id = data['id'],is_available = False)
                                city.is_available = True
                                city.save()
                                resp = Response(200,"City activated successfuly")
                                return JsonResponse(resp,status = 200)
                        except:
                                resp = Response(203,'city doesnot exist')
                                return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def modify_city(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'id','text','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        city = Master_City.objects.get(id = data['id'])
                        city.city_text = data['text']
                        city.save()
                        resp = Response(200,"City modified")
                        return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

@csrf_exempt
def add_city(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'text','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                city = Master_City.objects.get(city_text = data['text'])
                                resp = Response(203,'City already exists ')
                                return JsonResponse(resp, status  = 200)
                        except:
                                city = Master_City.objects.create(city_text = data['text'])
                                city.save()
                                resp = Response(200,"1")
                                return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)

# I am not updating user type id and email

@csrf_exempt
def update_user(request):
        if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                if {'auth_key','user_id','f_name','m_name','l_name','address1','address2','phone','city_id'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                user_obj = Master_Users.objects.get(id = data['user_id'],is_available = True)
                                city_obj = Master_City.objects.get(id = data['city_id'],is_available = True)
                        except Master_Users.DoesNotExist:
                                resp = Response(203,"user doesnot exists")
                                return JsonResponse(resp,status = 200)
                        except Master_City.DoesNotExist:
                                resp = Response(203,"city doesnot exists")
                                return JsonResponse(resp,status = 200)
                        user_obj.first_name = data['f_name']
                        user_obj.last_name = data['l_name']
                        user_obj.middle_name = data['m_name']
                        user_obj.address1 = data['address1']
                        user_obj.address2 = data['address2']
                        user_obj.city = city_obj
                        user_obj.phone = data['phone']
                        user_obj.save()
                        resp = Response(200,"user updated successfully")
                        return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_user_perman(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'user_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                user_obj = Master_Users.objects.get(id = data['user_id'])
                                user_cred_obj = User_Credentials.objects.get(user = user_obj)
                        except:
                                resp = Response(203,'User does not exists')
                                return JsonResponse(resp,status  = 200)

                        user_obj.delete()

                        resp = Response(200,'User deleted successfully ')
                        return JsonResponse(resp,status = 200)


        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


@csrf_exempt
def delete_group_perman(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'group_id','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                group_obj = Master_Groups.objects.get(id = data['group_id'],is_available = True)
                        except:
                                resp = Response(203,'Group doesnot exists')
                                return JsonResponse(resp,status  = 200)

                        group_obj.delete()
                        resp = Response(200,'Group deleted successfully ')
                        return JsonResponse(resp,status = 200)

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)


# import random, string
# x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
# print(x)

@csrf_exempt
def forget_password(request):
        if request.method == "POST":
                data = json.loads(request.body.decode('utf-8'))
                if {'email','auth_key'}.issubset(data.keys()) and authenticate(data['auth_key']):
                        try:
                                user_obj = Master_Users.objects.get(email = data['email'])
                                user_cred = User_Credentials.objects.get(user = user_obj)
                                random_pass = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
                                print(random_pass)
                                sendEmail_forgot_password(user_cred.user_name,data['email'],random_pass)
                                user_cred.password = random_pass
                                user_cred.save()
                                resp = Response(200,"Password sent")
                                return JsonResponse(resp,status = 200)



                        except:
                                resp = Response(203,'User doesnot exist') 
                                return JsonResponse(resp,status = 200)       

        resp = Response(405,'Bad Request!!')
        return JsonResponse(resp,status = 405)
                

#_-----------------------UTILS--------------------------------------------------------------


def get_group_dict(group):

        group_mappings = User_Group_Mapping.objects.filter(group = group)
        group_admin_dict = get_user_dict(group.group_admin)
        user_arr = []
        group_dict = {
                "group_id":group.id,
                "group_name":group.group_name,
                "is_available":group.is_available,
                "group_admin":group_admin_dict,
                "users_in_group":user_arr
        }
        for group_mapping in group_mappings:
                user = group_mapping.user
                user_arr.append(get_user_dict(user))
        return group_dict





def get_user_dict(user):
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
                'is_available': user.is_available,
                'city':{
                'name':city.city_text,
                'id' : city.id,
                },
        }
        return user_dict
