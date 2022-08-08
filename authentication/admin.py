from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class EmployeeInline(admin.StackedInline):
    """Custom InLine Model to add Employee to User in the Admin page"""
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employees'


class EmployeeUserAdmin(UserAdmin):
    """Custom UserAdmin page"""
    inlines = (EmployeeInline, )
    ordering = ('email', )
    exclude = ('username',)

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': (
        'is_active', 'is_staff', 'is_superuser', 'groups',
        'user_permissions')}),
    )


admin.site.register(User, EmployeeUserAdmin)
