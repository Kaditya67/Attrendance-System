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
    
    # Student Update
    path('update/student/', views.update_student, name='update_student'),

    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('hod/dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('principal/dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Attendance
    path('mark_attendance/', views.attendance, name='mark_attendance'),
    
    # Course Management
    path('course/enrollment/', views.course_enrollment, name='course_enrollment'),
    # path('course/management/', views.course_management, name='course_management'),
    
    # Lecture Scheduling
    # path('lecture/schedule/', views.lecture_scheduling, name='schedule_lecture'),
    
    # Attendance Reporting
    # path('attendance/report/', views.attendance_reporting, name='attendance_reporting'),
    # path('attendance/create/', views.create_attendance, name='create_attendance'),
    path('attendance/update/<int:pk>/', views.update_attendance, name='update_attendance'),
    
    # Password Reset
    # path('password/reset/', views.password_reset, name='password_reset'),
    
    # View Details
    path('view/student/details/', views.view_student_details, name='view_student_details'),
    path('view/teacher/details/', views.view_teacher_details, name='view_teacher_details'),
    
    # Miscellaneous
    path('success/', views.success, name='success'),
    path('no_permission/', views.no_permission, name='no_permission'),
]
