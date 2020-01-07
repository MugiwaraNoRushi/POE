from django.db import models

class Master_Users(models.Model):
    first_name = models.CharField(max_length = 255,default = " ")
    middle_name = models.CharField(max_length = 255,default = " ")
    last_name = models.CharField(max_length = 255, default = " " )
    email = models.EmailField(default = " ")
    phone = models.CharField(max_length = 20 , default = " ")
    address1 = models.TextField(default = " ")
    address2 = models.TextField(default = " ")
    city = models.ForeignKey('Master_City', on_delete=models.SET_NULL, null=True)
    user_type_id = models.SmallIntegerField(default=3)
    is_available = models.BooleanField(default= True)

class Master_City(models.Model):
    city_text = models.CharField(max_length = 100)
    is_available = models.BooleanField(default= True)

class User_Credentials(models.Model):
    user = models.ForeignKey('Master_Users',on_delete = models.SET_NULL, null = True)
    user_name = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    is_active = models.BooleanField(default= True)

class Temp_Master_Users(models.Model):
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    first_name = models.CharField(max_length = 255)
    middle_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField()
    phone = models.CharField(max_length = 20)
    address1 = models.TextField()
    address2 = models.TextField(default = " ")
    city = models.ForeignKey('Master_City', on_delete=models.SET_NULL, null=True)
    user_type_id = models.SmallIntegerField(default=3)
    entry_time = models.DateTimeField()
    registration_code = models.IntegerField()

class Master_Groups(models.Model):
    group_name = models.CharField(max_length = 255)
    is_available = models.BooleanField(default= True)
    group_admin = models.ForeignKey('Master_Users',on_delete = models.SET_NULL, null = True)

class User_Group_Mapping(models.Model):
    user = models.ForeignKey('Master_Users',on_delete = models.SET_NULL, null = True)
    group = models.ForeignKey('Master_Groups',on_delete = models.SET_NULL, null = True)
    
