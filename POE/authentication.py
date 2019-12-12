import json
import random
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Users.utils import Response
from datetime import datetime

#GLOBAL KEY
AUTH_KEY = None

@csrf_exempt
def create_key(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        token = data['token']
        if match_token(token):
            global AUTH_KEY
            AUTH_KEY = random.randint(1000000000,9999999999)
            dict = {
                'auth_key':AUTH_KEY
            }
            return JsonResponse(dict,status = 200)
    resp = Response(400,'Bad Request')
    return JsonResponse(resp)

@csrf_exempt
def send_key(request):
    if (AUTH_KEY == None):
        resp = Response(400,'no key found')
        return JsonResponse(resp)
    else:
        dict = {
            'auth_key':AUTH_KEY
        }
        return JsonResponse(dict,status = 200)


#-------------------UTILS-------------------------------------------------------------------


def authenticate(key):
    print('authenticate method called')
    if key == AUTH_KEY:
        return True
    else:
        return False



def match_token(token):
    time = str(datetime.now()).split('-')
    month = time[1]
    date = time[2].split(':')[0][:2]
    hour = time[2].split(':')[0][3:5]
    minute = time[2].split(':')
 
    if (token[4:6] == month):
        if token[6:8] == date:
            return True
            # if int(token[0:4]) == month*minute:
            #     if int(token[12:16]) == date*hour:
            #         return True
    
    return False