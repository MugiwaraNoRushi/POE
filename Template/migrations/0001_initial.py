# Generated by Django 2.2.3 on 2019-07-17 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master_Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=255)),
                ('section_marks', models.FloatField()),
                ('section_duration', models.TimeField()),
                ('negative_marks', models.FloatField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=255)),
                ('template_marks', models.FloatField()),
                ('template_duration', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Template_Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Template.Master_Section')),
                ('subtopic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Topics.Master_SubTopic')),
            ],
        ),
        migrations.AddField(
            model_name='master_section',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Template.Master_Template'),
        ),
    ]
