from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Master_City)
admin.site.register(Master_Users)
admin.site.register(Temp_Master_Users)
admin.site.register(Master_Groups)
admin.site.register(User_Group_Mapping)
admin.site.register(User_Credentials)