from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Permission

from .models import *


class EmployeeInline(admin.StackedInline):
    """Custom InLine Model to integrate Employee-info
    into User-Admin page"""
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employees'
    max_num = 1


class TeamMembershipInline(admin.StackedInline):
    """Custom Inline Model to integrate the team membership
     into the User-Admin page"""
    model = TeamMembership
    can_delete = False
    verbose_name = 'Team'
    max_num = 1
    autocomplete_fields = ['team', ]

    def get_formset(self, request, obj=None, **kwargs):
        """method modified to remove unwanted widget options"""
        formset = super(
            TeamMembershipInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['team'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset


class EmployeeUserAdmin(UserAdmin):
    """Custom UserAdmin page"""
    inlines = (TeamMembershipInline, EmployeeInline,)
    ordering = ('email', )
    exclude = ('username',)

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # ('Permissions', {'fields': (
        # 'is_active', 'is_staff', 'is_superuser', 'groups',
        # 'user_permissions')}),
    )
    add_fieldsets = (
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'email', 'password1', 'password2')}),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['labels'] = {'groups': 'Teams'}
        return super().get_form(request, obj, change=change, **kwargs)


admin.site.register(User, EmployeeUserAdmin)

admin.site.unregister(Group)
admin.site.register(Team, GroupAdmin)
admin.site.register(TeamMembership)
