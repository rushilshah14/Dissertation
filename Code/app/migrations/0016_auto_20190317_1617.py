# Generated by Django 2.1.7 on 2019-03-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20190305_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduledata',
            name='approved',
            field=models.IntegerField(default=0),
        ),
    ]
