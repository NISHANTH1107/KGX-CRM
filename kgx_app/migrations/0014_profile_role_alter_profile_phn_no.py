# Generated by Django 5.1 on 2024-10-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kgx_app', '0013_delete_hackathon'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('staff', 'Staff')], default='student', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phn_no',
            field=models.CharField(max_length=15),
        ),
    ]
