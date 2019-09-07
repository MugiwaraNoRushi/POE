# Generated by Django 2.2.3 on 2019-07-17 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Master_City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_text', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=' ', max_length=255)),
                ('middle_name', models.CharField(default=' ', max_length=255)),
                ('last_name', models.CharField(default=' ', max_length=255)),
                ('email', models.EmailField(default=' ', max_length=254)),
                ('phone', models.CharField(default=' ', max_length=20)),
                ('address1', models.TextField(default=' ')),
                ('address2', models.TextField(default=' ')),
                ('user_type_id', models.SmallIntegerField(default=3)),
                ('is_available', models.BooleanField(default=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Users.Master_City')),
            ],
        ),
        migrations.CreateModel(
            name='User_Group_Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Users.Master_Groups')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Users.Master_Users')),
            ],
        ),
        migrations.CreateModel(
            name='User_Credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Users.Master_Users')),
            ],
        ),
        migrations.CreateModel(
            name='Temp_Master_Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('address1', models.TextField()),
                ('address2', models.TextField(default=' ')),
                ('user_type_id', models.SmallIntegerField()),
                ('entry_time', models.TimeField()),
                ('registration_code', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Users.Master_City')),
            ],
        ),
    ]
