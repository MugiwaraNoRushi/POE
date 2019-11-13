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
    path('add/user/group/',add_user_to_group,name = "add user to group"),
    path('get/group/',get_group,name = 'get a single group'),
    path('get/all/groups/',get_all_groups,name = 'get all groups'),
    path('get/all/cities/',get_all_cities,name = 'get all cities'),
    path('add/city/',add_city,name = 'add city'),
    path('delete/city/',delete_city,name = 'delete city'),
    path('change/city/',modify_city,name = 'change city'),
    path('activate/city/',activate_city,name = 'activate a city'),
    path('get/all/users/',get_all_users,name = 'get all users'),
]