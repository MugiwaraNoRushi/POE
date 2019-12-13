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
            AUTH_KEY = random.randint(100000000000,999999999999)
            dict = {
                'auth_key':AUTH_KEY
            }
            return JsonResponse(dict,status = 200)
    resp = Response(400,'Bad Request')
    return JsonResponse(resp)


#-------------------UTILS-------------------------------------------------------------------


def authenticate(key):
    print('authenticate method called')
    if key == AUTH_KEY:
        return True
    else:
        return False



def match_token(token):
    time = str(datetime.now()).split('-')
    month = int(str(time[1]))
    date = int(str(time[2].split(':')[0][:2]))
    hour = int(str(time[2].split(':')[0][3:5]))
    minute = int(str(time[2].split(':')[1]))
 
    if (token[4:6] == date):
        print('date')
        if token[6:8] == month:
            print('month')
            first_val = int(str(token[0:4]))
            print(first_val)
            hour_t = int(str(token[8:10]))
            print(hour_t)
            minute_t = int(str(token[10:12]))
            print(minute_t)
            last_val = int(str(token[12:16]))
            print(last_val)
            if ((hour*60 + minute) - (hour_t*60 + minute_t)) <= 1:
                print('time')
                hour = hour_t
                minute = minute_t
                if first_val == month*minute:
                    print('first value')
                    if last_val == date*hour:
                        print('second value')
                        return True
                        print('true')
    print('false')
    return False