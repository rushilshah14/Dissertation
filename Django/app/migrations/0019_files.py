# Generated by Django 2.1.7 on 2019-04-12 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20190323_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('document', models.FileField(upload_to='formFiles/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('ecfdata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.EcfData')),
            ],
        ),
    ]
