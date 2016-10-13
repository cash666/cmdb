from django.contrib import admin
from web import models
# Register your models here.
admin.site.register(models.Idc)
admin.site.register(models.HostList)
admin.site.register(models.Assets)
admin.site.register(models.Group)
admin.site.register(models.Upload)
admin.site.register(models.UserProfile)
admin.site.register(models.UserGroup)
