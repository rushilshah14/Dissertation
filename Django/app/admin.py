from django.contrib import admin
from app.models import UserProfile, EcfData, ModuleData
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(EcfData)
admin.site.register(ModuleData)
