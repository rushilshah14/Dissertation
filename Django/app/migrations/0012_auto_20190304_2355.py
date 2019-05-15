# Generated by Django 2.1.7 on 2019-03-04 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20190304_2344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moduledata',
            name='form',
        ),
        migrations.AddField(
            model_name='moduledata',
            name='ecfdata',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.EcfData'),
            preserve_default=False,
        ),
    ]