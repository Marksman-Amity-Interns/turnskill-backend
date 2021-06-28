from django.contrib import admin
from .models import *
# Register your models here.

# @admin.register(user)
# class user(admin.ModelAdmin):
#     list_display = ['id', 'email']
admin.site.register(user)
admin.site.register(course)
admin.site.register(feedback)
admin.site.register(video)
admin.site.register(skill)
admin.site.register(notes)
admin.site.register(enrolment)