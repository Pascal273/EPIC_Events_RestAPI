from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from .models import *


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
    inlines = (TeamMembershipInline, )
    ordering = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    exclude = ('username',)

    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'is_active')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'password', 'phone',
                       'mobile', 'hire_date', 'birth_date')}),
        ('Other Dates', {
            'fields': ('last_login', 'joined')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            # 'groups',
            'user_permissions'
        )}),
    )
    readonly_fields = ['is_staff', 'is_superuser', 'user_permissions']
    add_fieldsets = (
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'email', 'phone', 'birth_date',
            'password1', 'password2')}),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['labels'] = {'groups': 'Teams'}
        return super().get_form(request, obj, change=change, **kwargs)


admin.site.register(User, EmployeeUserAdmin)

admin.site.unregister(Group)
admin.site.register(Team, GroupAdmin)
admin.site.register(TeamMembership)

# custom changes to admin page:
admin.site.site_header = 'Epic-Events administration'
