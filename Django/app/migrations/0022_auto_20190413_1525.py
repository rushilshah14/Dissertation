# Generated by Django 2.1.7 on 2019-04-13 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_publicecf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicecf',
            old_name='detailecf',
            new_name='publicecf',
        ),
    ]
