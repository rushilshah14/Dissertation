# Generated by Django 2.1.7 on 2019-04-15 14:23

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_ecfdata_moreproof'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='userlink',
            field=models.CharField(default=app.models.randomlinks, max_length=15),
        ),
    ]
