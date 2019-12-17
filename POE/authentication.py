import json
import random
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Users.utils import Response
from datetime import datetime
from pytz import timezone

#GLOBAL KEY
AUTH_KEY = None

@csrf_exempt
def create_key(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        token = data['token']
        if match_token(token):
            global AUTH_KEY
            AUTH_KEY = str(random.randint(100000000000,999999999999))
            dict = {
                'auth_key':AUTH_KEY
            }
            return JsonResponse(dict,status = 200)
    resp = Response(400,'Bad Request')
    return JsonResponse(resp)


#-------------------UTILS-------------------------------------------------------------------


def authenticate(key):
    if key == AUTH_KEY:
        return True
    else:
        return False



def match_token(token):
    time = str(datetime.now(timezone('Asia/Kolkata'))).split('-')
    month = int(str(time[1]))
    date = int(str(time[2].split(':')[0][:2]))
    hour = int(str(time[2].split(':')[0][3:5]))
    minute = int(str(time[2].split(':')[1]))
    date_t = int(str(token[4:6]))
    month_t = int(str(token[6:8]))
    if (date_t == date):
        if month_t == month:
            first_val = int(str(token[0:4]))
            hour_t = int(str(token[8:10]))
            minute_t = int(str(token[10:12]))
            last_val = int(str(token[12:16]))
            if ((hour*60 + minute) - (hour_t*60 + minute_t)) <= 1:
                hour = hour_t
                minute = minute_t
                if first_val == date*minute:
                    if last_val == month*hour:
                        return True
    return False