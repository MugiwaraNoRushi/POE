# Generated by Django 2.2.3 on 2020-01-27 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0011_master_subscription_user_subscription_mapping'),
    ]

    operations = [
        migrations.RenameField(
            model_name='master_subscription',
            old_name='count',
            new_name='count_or_no_days',
        ),
        migrations.RemoveField(
            model_name='master_subscription',
            name='no_days',
        ),
    ]
