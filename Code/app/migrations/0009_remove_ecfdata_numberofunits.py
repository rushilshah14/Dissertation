# Generated by Django 2.1.7 on 2019-03-04 03:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20190304_0305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecfdata',
            name='numberofunits',
        ),
    ]
