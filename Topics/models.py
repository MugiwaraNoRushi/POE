from django.db import models

class Master_Topic(models.Model):
    topic_text = models.CharField(max_length = 100)
    is_available = models.BooleanField(default= True)

class Master_SubTopic(models.Model):
    subtopic_text = models.CharField(max_length = 100)
    topic = models.ForeignKey('Master_Topic',on_delete = models.SET_NULL,null = True)
    is_available = models.BooleanField(default= True)