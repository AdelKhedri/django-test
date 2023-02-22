from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profiel
# Register your models here.

admin.site.register(User, UserAdmin)
UserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name' ,'email' , 'phone_number', 'is_report_time')
UserAdmin.list_display += ('is_report_time',)
admin.site.register(Profiel)