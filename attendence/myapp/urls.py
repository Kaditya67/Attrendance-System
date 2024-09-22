from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User Registration
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('register/hod/', views.register_hod, name='register_hod'),
    path('register/staff/', views.register_staff, name='register_staff'),
    path('register/principal/', views.register_principal, name='register_principal'),
    
    path('update/student', views.update_student, name='update_student'),

    # Dashboards
    path('student_form',views.student_form,name='student_form'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.dash_teacher, name='dash_teacher'),
    path('hod/dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('principal/dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Attendance
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    
    # Course Management
    path('course/enrollment/', views.course_enrollment, name='course_enrollment'),
    path('course/management/', views.course_management, name='course_management'),
    
    # Lecture Scheduling
    path('lecture/schedule/', views.lecture_scheduling, name='schedule_lecture'),
    
    # Attendance Reporting
    path('attendance/report/', views.attendance_reporting, name='attendance_reporting'),
    
    # Profile Management
    # path('profile/update/', views.profile_update, name='profile_update'),
    
    # Password Reset
    path('password/reset/', views.password_reset, name='password_reset'),
    
    # View Details
    path('view/student/details/', views.view_student_details, name='view_student_details'),
    path('view/teacher/details/', views.view_teacher_details, name='view_teacher_details'),
    
    # Miscellaneous
    path('success/', views.success, name='success'),
    path('no_permission/', views.no_permission, name='no_permission'),
    # path('', views.index, name='index'),
    path('demo/', views.demo_dash, name='demo_dash'),
    path('view_grades/', views.view_grades, name='view_grades'),
    path('manage_teachers/', views.manage_teachers, name='manage_teachers'),
]









# from django.contrib import admin
# # from django.urls import path
# # from .views import (
# #     index, no_permission, 
# #     register_student,
# #     register_teacher, register_hod, register_staff,
# #     register_principal, login_view, logout_view, success,
# #     dashboard, student_dashboard, mark_attendance, 
# #     principal_dashboard, hod_dashboard, staff_dashboard, 
# #     view_teacher_details, manage_teachers, view_student_details, view_grades,
# #     dash_teacher, demo_dash,
# #     #   principal
# # )

# urlpatterns = [
#     # Authentication URLs
#     # path('login/', login_view, name='login'),
#     # path('logout/', logout_view, name='logout'),

#     # # Registration URLs
#     # path('register/student/', register_student, name='register_student'),
#     # path('register/teacher/', register_teacher, name='register_teacher'),
#     # path('register/hod/', register_hod, name='register_hod'),
#     # path('register/staff/', register_staff, name='register_staff'),
#     # path('register/principal/', register_principal, name='register_principal'),

#     # # Success URL
#     # path('success/', success, name='success'),

#     # # Dashboard URLs
#     # path('dashboard/', dashboard, name='dashboard'),
#     # path('student_dashboard/', student_dashboard, name='student_dashboard'),
#     # path('principal_dashboard/', principal_dashboard, name='principal_dashboard'),
#     # path('hod_dashboard/', hod_dashboard, name='hod_dashboard'),
#     # path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
#     # path('dash_teacher/', dash_teacher, name='dash_teacher'),
#     # path('demo_dash/', demo_dash, name='demo_dash'),

#     # # Attendance and Grades URLs
#     # path('mark_attendance/', mark_attendance, name='mark_attendance'),
#     # path('view_grades/', view_grades, name='view_grades'),

#     # # HOD and Principal-specific URLs
#     # path('view_teacher_details/', view_teacher_details, name='view_teacher_details'),
#     # path('manage_teachers/', manage_teachers, name='manage_teachers'),
#     # path('view_student_details/', view_student_details, name='view_student_details'),

#     # # Permissions URLs
#     # path('no_permission/', no_permission, name='no_permission'),

#     # # Home
#     # path('', index, name='index'),

#     # Principal
#     # path('principal/', principal, name='principal'),
# ]


# # from django.contrib import admin
# # from django.urls import path
# # from .views import (
# #     index, no_permission, 
# #     register_student,
# #     register_teacher, register_hod, register_staff,
# #     register_principal, login_view, logout_view, success,
# #     dashboard, student_dashboard, mark_attendance, 
# #     principal_dashboard, hod_dashboard, staff_dashboard, 
# #     view_teacher_details, manage_teachers, view_student_details, view_grades,
# #     dash_teacher, demo_dash, principal
# # )

# # urlpatterns = [
# #     # Authentication URLs
# #     path('login/', login_view, name='login'),
# #     path('logout/', logout_view, name='logout'),

# #     # Registration URLs
# #     path('register/student/', register_student, name='register_student'),
# #     path('register/teacher/', register_teacher, name='register_teacher'),
# #     path('register/hod/', register_hod, name='register_hod'),
# #     path('register/staff/', register_staff, name='register_staff'),
# #     path('register/principal/', register_principal, name='register_principal'),

# #     # Success URL
# #     path('success/', success, name='success'),
# #     path('dashboard/', dashboard, name='dashboard'),

# #     # Dashboard URLs
# #     path('student_dashboard/', student_dashboard, name='student_dashboard'),
# #     path('principal_dashboard/', principal_dashboard, name='principal_dashboard'),
# #     path('hod_dashboard/', hod_dashboard, name='hod_dashboard'),
# #     path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
# #     path('dash_teacher/', dash_teacher, name='dash_teacher'),
# #     path('demo_dash/', demo_dash, name='demo_dash'),

# #     # Attendance and Grades URLs
# #     path('mark_attendance/', mark_attendance, name='mark_attendance'),
# #     path('view_grades/', view_grades, name='view_grades'),

# #     # HOD and Principal-specific URLs
# #     path('view_teacher_details/', view_teacher_details, name='view_teacher_details'),
# #     path('manage_teachers/', manage_teachers, name='manage_teachers'),
# #     path('view_student_details/', view_student_details, name='view_student_details'),

# #     # Permissions URLs
# #     path('no_permission/', no_permission, name='no_permission'),

# #     # Home
# #     path('', index, name='index'),

# #     # Principal
# #     # path('principal/', principal, name='principal'),
# # ]
