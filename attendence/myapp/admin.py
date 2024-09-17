from django.contrib import admin
from .models import Department, Student, Teacher, Attendance

# Registering the Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # Ensure 'created_at' exists in Department model
    search_fields = ('name',)

# Registering the Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department', 'year')  # Ensure 'year' exists in Student model
    list_filter = ('department', 'year')  # Ensure 'year' exists and is a valid field
    search_fields = ('user__username', 'roll_number')
    ordering = ('roll_number',)

# Registering the Teacher model
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'department__name')
    list_filter = ('department',)
    ordering = ('user__username',)

# Registering the Attendance model
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'date', 'status')  # Ensure 'status' exists in Attendance model
    list_filter = ('date', 'status')  # Ensure 'status' is a valid field
    search_fields = ('student__user__username', 'teacher__user__username')
    ordering = ('date',)


from .models import Year
admin.site.register(Year)