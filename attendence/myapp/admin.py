from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Principal, HOD, Teacher, Staff, Student

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)

class PrincipalAdmin(admin.ModelAdmin):
    list_display = ('user', 'office_location', 'department')
admin.site.register(Principal, PrincipalAdmin)

class HODAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'office_number', 'managing_teachers')
admin.site.register(HOD, HODAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'program', 'faculty_id')
admin.site.register(Teacher, TeacherAdmin)

class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'assigned_department', 'staff_id')
admin.site.register(Staff, StaffAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'roll_number', 'year_of_study', 'cgpa')
admin.site.register(Student, StudentAdmin)
