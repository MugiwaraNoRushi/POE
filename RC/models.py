from django.db import models

class Master_RC(models.Model):
    rc_text = models.TextField()
    is_available = models.BooleanField(default= True)

class RC_Question_Mapping(models.Model):
    question = models.ForeignKey('Questions.Master_Question',on_delete = models.SET_NULL, null = True)
    rc = models.ForeignKey('Master_RC', on_delete = models.SET_NULL, null = True)