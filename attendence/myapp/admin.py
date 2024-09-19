from django.contrib import admin
from .models import (
    Department, Principal, Staff, Student, Teacher, Attendance, 
    # OddSem, EvenSem, 
    SemesterCGPA, LabsBatches, Program, Lecture, HOD, Course, Year
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
    list_display = ('user', 'roll_number', 'department', 'year')  # Corrected typo from 'list_displaStaffly' to 'list_display'
    list_filter = ('department', 'year')  # Ensure 'year' exists and is valid
    search_fields = ('user__username', 'roll_number')
    ordering = ('roll_number',)

# Registering the Teacher model
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'faculty_id')  # Added faculty ID for clarity
    search_fields = ('user__username', 'department__name', 'faculty_id')  # Added faculty ID to search
    list_filter = ('department',)
    ordering = ('user__username',)

# Registering the Attendance model with custom teacher display
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher_name', 'date', 'status')  # Custom method for displaying teacher's name
    list_filter = ('date', 'status')  # Ensure 'status' exists in Attendance model
    search_fields = ('student__user__username', 'teacher__user__username')  # Assuming teacher is a field
    ordering = ('date',)

    # Method to retrieve teacher's name via course relationship
    def teacher_name(self, obj):
        teachers = obj.course.teachers.all()  # Assuming a ManyToMany relationship
        if teachers.exists():
            return ', '.join([teacher.user.username for teacher in teachers])
        return 'No Teacher Assigned'

    teacher_name.short_description = 'Teacher'

# Registering the remaining models with basic admin setup
@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(SemesterCGPA)
class SemesterCGPAAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'cgpa')
    search_fields = ('student__user__username', 'semester__name')
    list_filter = ('semester',)
    ordering = ('semester',)

# @admin.register(OddSem)
# class OddSemAdmin(admin.ModelAdmin):
#     list_display = ('semester_number', 'program')
#     search_fields = ('semester_number', 'program__name')
#     list_filter = ('program',)

# @admin.register(EvenSem)
# class EvenSemAdmin(admin.ModelAdmin):
#     list_display = ('semester_number', 'program')
#     search_fields = ('semester_number', 'program__name')
#     list_filter = ('program',)

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('program', 'course', 'date')
    search_fields = ('program__name', 'course__name')
    list_filter = ('date', 'program')
    ordering = ('date',)

@admin.register(LabsBatches)
class LabsBatchesAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'department')
    search_fields = ('name', 'program__name', 'department__name')
    list_filter = ('department', 'program')
    ordering = ('name',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'get_semester')  # Custom method for semester
    search_fields = ('name', 'department__name')
    list_filter = ('department',)

    # Custom method to display semester
    def get_semester(self, obj):
        return obj.semester if obj.semester else 'No Semester'

    get_semester.short_description = 'Semester'


@admin.register(HOD)
class HODAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'office_number')
    search_fields = ('user__username', 'department__name')
    list_filter = ('department',)
    ordering = ('user__username',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'assigned_department')
    search_fields = ('user__username', 'position', 'assigned_department__name')
    list_filter = ('assigned_department',)
    ordering = ('user__username',)


@admin.register(Principal)
class PrincipalAdmin(admin.ModelAdmin):
    list_display = ('user', 'office_location')  # Only display relevant fields
    search_fields = ('user__username', 'office_location')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)
