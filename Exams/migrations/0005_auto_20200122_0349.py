# Generated by Django 2.2.3 on 2020-01-22 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Exams', '0004_user_test_status_attempts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_exam',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Users.Master_Groups'),
        ),
        migrations.AlterField(
            model_name='master_exam',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Template.Master_Template'),
        ),
        migrations.AlterField(
            model_name='user_question_assigned',
            name='exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Exams.Master_Exam'),
        ),
        migrations.AlterField(
            model_name='user_question_assigned',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questions.Master_Question'),
        ),
        migrations.AlterField(
            model_name='user_question_assigned',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Template.Master_Section'),
        ),
        migrations.AlterField(
            model_name='user_question_assigned',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Users.Master_Users'),
        ),
        migrations.AlterField(
            model_name='user_question_response',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questions.Master_Option'),
        ),
        migrations.AlterField(
            model_name='user_question_response',
            name='section_question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Exams.User_Question_Assigned'),
        ),
        migrations.AlterField(
            model_name='user_test_status',
            name='exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Exams.Master_Exam'),
        ),
        migrations.AlterField(
            model_name='user_test_status',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Users.Master_Users'),
        ),
    ]
