from django.db import models

class Master_Exam(models.Model):
    exam_name = models.CharField(max_length = 255)
    exam_duration = models.IntegerField()
    group = models.ForeignKey('Users.Master_Groups',on_delete = models.CASCADE,null = True)
    template = models.ForeignKey('Template.Master_Template',on_delete = models.CASCADE,null = True)
    show_result_immediately = models.BooleanField(default= False)
    result_timestamp = models.DateTimeField()
    exam_enable_time = models.DateTimeField()
    is_enable = models.BooleanField(default= True)
    is_available = models.BooleanField(default= True)

class User_Question_Assigned(models.Model):
    section = models.ForeignKey('Template.Master_Section',on_delete = models.CASCADE,null = True)
    question = models.ForeignKey('Questions.Master_Question',on_delete = models.CASCADE,null = True)
    exam = models.ForeignKey('Master_Exam',on_delete = models.CASCADE,null = True)
    user = models.ForeignKey('Users.Master_Users',on_delete = models.CASCADE,null = True)

class User_Question_Response(models.Model):
    section_question = models.ForeignKey('User_Question_Assigned',on_delete = models.CASCADE,null = True)
    option = models.ForeignKey('Questions.Master_Option',on_delete = models.CASCADE,null = True)
    marked = models.BooleanField(default = False)

class User_Test_Status(models.Model):
    exam = models.ForeignKey('Master_Exam',on_delete = models.CASCADE,null = True)
    user = models.ForeignKey('Users.Master_Users',on_delete = models.CASCADE,null = True)
    status = models.SmallIntegerField() #1 not started 2 in progress 3 completed
    duration = models.IntegerField()
    attempts = models.SmallIntegerField(default = 3)
