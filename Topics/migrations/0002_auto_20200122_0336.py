# Generated by Django 2.2.3 on 2020-01-22 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Topics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_subtopic',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Topics.Master_Topic'),
        ),
    ]
