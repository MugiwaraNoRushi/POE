from django.db import models

class Master_Template(models.Model):
    template_name = models.CharField(max_length = 255)
    template_marks = models.FloatField()
    template_duration = models.IntegerField()
    is_available = models.BooleanField(default= True)

class Master_Section(models.Model):
    section_name = models.CharField(max_length = 255)
    template = models.ForeignKey('Master_Template',on_delete = models.SET_NULL, null =True)
    section_marks = models.FloatField()
    section_duration = models.IntegerField()
    negative_marks = models.FloatField()
    is_available = models.BooleanField(default= True)

class Template_Section(models.Model):
    section = models.ForeignKey('Master_Section',on_delete = models.SET_NULL,null =True)
    subtopic = models.ForeignKey('Topics.Master_SubTopic',on_delete = models.SET_NULL, null = True)  
    no_questions = models.IntegerField()
    difficulty_id = models.SmallIntegerField()  


