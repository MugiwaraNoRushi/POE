from django.db import models

class Master_DI(models.Model):
    di_text = models.TextField()
    is_available = models.BooleanField(default= True)

class DI_Question_Mapping(models.Model):
    question = models.ForeignKey('Questions.Master_Question',on_delete = models.SET_NULL, null = True)
    di = models.ForeignKey('Master_DI', on_delete = models.SET_NULL, null = True)