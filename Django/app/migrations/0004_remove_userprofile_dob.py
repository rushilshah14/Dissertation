# Generated by Django 2.1.7 on 2019-02-25 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_userprofile_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dob',
        ),
    ]