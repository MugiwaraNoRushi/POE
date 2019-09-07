from django.urls import path
from Users.views import *



urlpatterns = [
    path('login/',validate,name = "validate credentials"),
    path('signup/',signup,name = 'signup'),
    path('validate/registration/',validate_registration,name = 'validate registration'),
    path('check/username/',check_username,name = 'check username'),
    path('change/password/',change_password,name = 'change password'),
    path('get/user/',get_user,name = 'get user'),
    path('create/group/',create_group,name = "create group"),
    path('add/user/group/',add_user_to_group,name = "add user to group")
]