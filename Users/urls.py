from django.urls import path
from Users.views import *
from Users.subs_views import *


urlpatterns = [
    path('login/',validate,name = "validate credentials"),
    path('signup/',signup,name = 'signup'),
    path('validate/registration/',validate_registration,name = 'validate registration'),
    path('check/username/',check_username,name = 'check username'),
    path('change/password/',change_password,name = 'change password'),
    path('get/user/',get_user,name = 'get user'),
    path('get/userbyid/',get_user_by_id,name = 'get user by id'),
    path('create/group/',create_group,name = "create group"),
    path('add/user/group/',add_user_to_group,name = "add user to group"),
    path('get/group/users',get_users_from_group,name = "get users from group"),
    path('get/user/groups',get_groups_from_user,name = "get groups from user"),
    path('get/group/',get_group,name = 'get a single group'),
    path('get/all/groups/',get_all_groups,name = 'get all groups'),
    path('remove/users/group/',remove_user_from_group,name = 'remove users from the group'),
    path('modify/group/',modify_group,name = 'modify a group name'),
    path('delete/group/',delete_group,name = 'delete a group'),
    path('activate/group/',activate_group,name = 'activate a group'),
    path('get/city/',get_city,name = 'get city'),
    path('get/all/cities/',get_all_cities,name = 'get all cities'),
    path('add/city/',add_city,name = 'add city'),
    path('delete/city/',delete_city,name = 'delete city'),
    path('change/city/',modify_city,name = 'change city'),
    path('activate/city/',activate_city,name = 'activate a city'),
    path('get/all/users/',get_all_users,name = 'get all users'),
    path('delete/user/',delete_user,name = 'delete a user'),
    path('activate/user/',activate_user,name = 'activate a user'),
    path('update/user/',update_user,name = 'update a user'),
    path('delete/user/perman/',delete_user_perman,name = 'delete a user permanently'),
    path('delete/group/perman/',delete_group_perman,name = 'delete a group permanently'),
    path('forget/password/',forget_password,name = 'forgot password and change it to temporary'),
    #subs_urls
    path('add/subscription/',create_subs,name = 'create master subscription'),
    path('update/subscription/',update_subs,name = 'update master subscription'),
    path('delete/subscription/',delete_subs,name = 'deactivate master subscription'),
    path('activate/subscription/',activate_subs,name = 'activate master subscription'),
    path('delete/subscription/perm/',delete_subs_perman,name = 'delete master subscription permanently'),
    path('get/subscription/',get_subs,name = 'get single master subscription'),
    path('add/subscription/for/user/',create_subs_users,name = 'create subs for user'),
    path('get/subscription/for/user/',get_user_subs,name = 'get single subscription'),
    path('get/all/subscriptions/for/user/by/user/',get_user_subs_subs_id,name = 'get all subscripitons by user'),
    path('get/subscriptions/for/user/by/subscription/',get_user_subs_subs_id,name ='get all subscripitons by subscriptions'),
    path('get/subscriptions/for/user/all/',get_user_subs_all,name ='get all subscriptions'),
    
]
