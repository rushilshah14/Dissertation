# Generated by Django 2.1.7 on 2019-03-04 01:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_auto_20190225_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='EcfData',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('ukvisa', models.IntegerField(default=0)),
                ('coursename', models.CharField(max_length=30)),
                ('studyyear', models.IntegerField()),
                ('numberofunits', models.IntegerField()),
                ('durationstartdate', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('durationenddate', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('circumstance', models.CharField(max_length=30)),
                ('detailecf', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleData',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('action', models.CharField(max_length=255)),
                ('unitcode', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=30)),
                ('startdate', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('enddate', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('approved', models.BooleanField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.EcfData')),
            ],
        ),
    ]
