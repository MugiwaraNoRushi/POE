# Generated by Django 2.2.3 on 2019-10-24 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_question_response',
            name='marked',
            field=models.BooleanField(default=False),
        ),
    ]
