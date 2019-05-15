from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from app.validators import validate_file_extension
import os, random

# Create your models here.

def randomlinks():
    chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr= ''.join((random.choice(chars)) for x in range(8))
    return randomstr

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, related_name='profile')
    userpower = models.IntegerField(default=1)
    userlink = models.CharField(default=randomlinks, max_length=15, unique=True)
    dob = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.user.username


class EcfData(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    ukvisa = models.IntegerField(default=0)
    coursename = models.CharField(max_length=255)
    studyyear = models.IntegerField(default=0)
    numberofunits = models.IntegerField(default=0)
    durationstartdate = models.DateTimeField(default=datetime.now, blank=True)
    durationenddate = models.DateTimeField(default=datetime.now, blank=True)
    circumstance = models.CharField(max_length=255)
    detailecf = models.CharField(max_length=10000)
    user = models.ForeignKey(User,on_delete = models.CASCADE, to_field='id')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    moreproof = models.BooleanField(default=False)


class ModuleData(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    action = models.CharField(max_length=255)
    unitcode = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    startdate = models.DateTimeField(default=datetime.now, blank=True)
    enddate = models.DateTimeField(default=datetime.now, blank=True)
    approved = models.IntegerField(default=0)
    ecfdata = models.ForeignKey(EcfData,on_delete = models.CASCADE, to_field='id')

def save_file_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr= ''.join((random.choice(chars)) for x in range(5))
    return 'formfiles/formid_{ecfid}/{basename}_{randomstring}{ext}'.format(ecfid= instance.ecfdata.id, basename= basefilename, randomstring= randomstr, ext= file_extension)

class Files(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    ecfdata = models.ForeignKey(EcfData,on_delete = models.CASCADE, to_field='id')
    document = models.FileField(upload_to=save_file_path, validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return self.document.name.split('/')[2]

class PublicEcf(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    publicecf = models.CharField(max_length=10000)
    user = models.OneToOneField(User,on_delete = models.CASCADE, to_field='id',unique=True)
