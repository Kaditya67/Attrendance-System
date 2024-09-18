from django.contrib import admin
from django.urls import path
from .views import (
    index, no_permission, 
    register_student,
    register_teacher, register_hod, register_staff,
    register_principal, login_view, logout_view, success,
    dashboard, student_dashboard, mark_attendance, 
    principal_dashboard, hod_dashboard, staff_dashboard, 
    view_teacher_details, manage_teachers, view_student_details, view_grades,
    dash_teacher, demo_dash
)

urlpatterns = [
    # Authentication URLs
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Registration URLs
    path('register/student/', register_student, name='register_student'),
    path('register/teacher/', register_teacher, name='register_teacher'),
    path('register/hod/', register_hod, name='register_hod'),
    path('register/staff/', register_staff, name='register_staff'),
    path('register/principal/', register_principal, name='register_principal'),

    # Success URL
    path('success/', success, name='success'),
    path('dashboard/', dashboard, name='dashboard'),

    # Dashboard URLs
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('principal_dashboard/', principal_dashboard, name='principal_dashboard'),
    path('hod_dashboard/', hod_dashboard, name='hod_dashboard'),
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
    path('dash_teacher/', dash_teacher, name='dash_teacher'),
    path('demo_dash/', demo_dash, name='demo_dash'),

    # Attendance and Grades URLs
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('view_grades/', view_grades, name='view_grades'),

    # HOD and Principal-specific URLs
    path('view_teacher_details/', view_teacher_details, name='view_teacher_details'),
    path('manage_teachers/', manage_teachers, name='manage_teachers'),
    path('view_student_details/', view_student_details, name='view_student_details'),

    # Permissions URLs
    path('no_permission/', no_permission, name='no_permission'),

    # Home
    path('', index, name='index'),
]
