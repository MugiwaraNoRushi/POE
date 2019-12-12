import json
import random
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

AUTH_KEY = None

@csrf_exempt
def create_key(request):
    AUTH_KEY = random.randint(1000000000,9999999999)
    dict = {
        'key':AUTH_KEY
    }
    return JsonResponse(dict,status = 200)