# Generated by Django 2.1.7 on 2019-03-05 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0013_auto_20190305_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecfdata',
            name='user',
        ),
        migrations.RemoveField(
            model_name='moduledata',
            name='ecfdata',
        ),
        migrations.AddField(
            model_name='ecfdata',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moduledata',
            name='ecfdata_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.EcfData'),
            preserve_default=False,
        ),
    ]