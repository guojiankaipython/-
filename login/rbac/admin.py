from django.contrib import admin

# Register your models here.

from rbac import models

class Permission(admin.ModelAdmin):
    list_display = ['id','url','title','menu','icon']
    list_editable = ['url','title','menu','icon']
# admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.Permission,Permission)


