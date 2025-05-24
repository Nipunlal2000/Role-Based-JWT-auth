from django.contrib import admin
from . models import *

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['email', 'role']

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'team_name', 'number_of_members']

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'can_create_managers']

@admin.register(SuperAdmin)
class SuperAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'assigned_project', 'date_joined_team']
