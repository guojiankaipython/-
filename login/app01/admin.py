from django.contrib import admin

# Register your models here.
from app01 import models

class User(admin.ModelAdmin):
    list_display = ['username','password','email','telephone','is_active']
    list_editable = ['password','email','telephone']

admin.site.register(models.User,User)
admin.site.register(models.Customer)
admin.site.register(models.Campuss)
admin.site.register(models.ClassList)
admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)