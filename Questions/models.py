from django.db import models

class Master_Question(models.Model):
    question_type = models.SmallIntegerField()
    question_text = models.TextField()
    question_marks = models.FloatField()
    subtopic = models.ForeignKey('Topics.Master_SubTopic',on_delete = models.CASCADE, null = True)
    difficulty = models.SmallIntegerField()
    is_available = models.BooleanField(default= True)

class Master_Option(models.Model):
    option_text = models.CharField(max_length = 500)
    question = models.ForeignKey('Master_Question',on_delete = models.CASCADE, null = True)
    is_available = models.BooleanField(default= True)

class Master_Correct_Option(models.Model):
    option = models.ForeignKey('Master_Option',on_delete = models.CASCADE, null = True)
    question = models.ForeignKey('Master_Question',on_delete = models.CASCADE, null = True)
    is_available = models.BooleanField(default= True)
    
