from django.contrib import admin
from .models import (
    Department, Principal, Staff, Student, Teacher, Attendance, 
    SemesterCGPA, LabsBatches, Program, Lecture, HOD, Course, 
    Year
)

# Registering the Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # Ensure 'created_at' exists in Department model
    search_fields = ('name',)
    ordering = ('name',)

# Registering the Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department', 'year')
    list_filter = ('department', 'year')
    search_fields = ('user__username', 'roll_number')
    ordering = ('roll_number',)

# Registering the Teacher model
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'faculty_id')
    search_fields = ('user__username', 'department__name', 'faculty_id')
    list_filter = ('department',)
    ordering = ('user__username',)

# Registering the Attendance model with custom teacher display
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'lab_batch', 'date', 'present')
    list_filter = ('date', 'present', 'course', 'student')
    search_fields = ('student__user__username', 'course__name', 'lab_batch__name')
    ordering = ('date',)

    def teacher_name(self, obj):
        teachers = obj.course.teachers.all()  # Assuming a ManyToMany relationship
        if teachers.exists():
            return ', '.join([teacher.user.username for teacher in teachers])
        return 'No Teacher Assigned'

    teacher_name.short_description = 'Teacher'

# Registering the Year model
@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

# Registering the SemesterCGPA model
@admin.register(SemesterCGPA)
class SemesterCGPAAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'cgpa')
    search_fields = ('student__user__username', 'semester__name')
    list_filter = ('semester',)
    ordering = ('semester',)

# Registering the Lecture model
@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('program', 'course', 'date')
    search_fields = ('program__name', 'course__name')
    list_filter = ('date', 'program')
    ordering = ('date',)

# Registering the LabsBatches model
@admin.register(LabsBatches)
class LabsBatchesAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'department')
    search_fields = ('name', 'program__name', 'department__name')
    list_filter = ('department', 'program')
    ordering = ('name',)

# Registering the Program model
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'department',)
    search_fields = ('name', 'department__name')
    list_filter = ('department',)

# Registering the HOD model
# @admin.register(HOD)
# class HODAdmin(admin.ModelAdmin):
#     list_display = ('user', 'department', 'office_number')
#     search_fields = ('user__username', 'department__name')
#     list_filter = ('department',)
#     ordering = ('user__username',)

# Registering the HOD model
admin.site.register(HOD)

# Registering the Staff model
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'assigned_department')
    search_fields = ('user__username', 'position', 'assigned_department__name')
    list_filter = ('assigned_department',)
    ordering = ('user__username',)

# Registering the Principal model
@admin.register(Principal)
class PrincipalAdmin(admin.ModelAdmin):
    list_display = ('user', 'office_location')
    search_fields = ('user__username', 'office_location')

# Registering the Course model
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


from .models import SessionYear, Semester
admin.site.register(SessionYear)
admin.site.register(Semester)