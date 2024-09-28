from django.urls import path
from . import views

urlpatterns = [
    #to do
    path('update_Attendance',views.update_Attendance,name='update_Attendance'), 
    path('fetch_students/', views.fetch_students, name='fetch_students'),
    path('Add_Attendance',views.Add_Attendance,name='Add_Attendance'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('SubjectDetails',views.SubjectDetails,name='SubjectDetails'),
    path('teacher_dashboard',views.Subject_Attendance_Details,name='Teacher_dashboard'),
    path('StudentDashBoard/<str:student_id>/',views.StudentDashBoard,name='StudentDashBoard'),
    path('PrincipalDashboard',views.PrincipalDashboard,name='PrincipalDashboard'),
    path('HOD_Dashboard',views.HOD_Dashboard,name='HOD_Dashboard'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('Delete_Attendance',views.Delete_Attendance,name='Delete_Attendance'),
    path('ClassDashboard',views.ClassDashboard,name='ClassDashboard'),
    path('Class_Report',views.Class_Report,name='Class_Report'),
    
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
    path('student_form/',views.student_form,name='student_form'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.dash_teacher, name='dash_teacher'),
    # Student Update
    path('update/student/', views.update_student, name='update_student'),

    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
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
    path('index/', views.index, name='index'),
    path('demo/', views.demo_dash, name='demo_dash'),
    path('view_grades/', views.view_grades, name='view_grades'),
    path('manage_teachers/', views.manage_teachers, name='manage_teachers'),

    path('courses/', views.manage_courses, name='course_list'),  # This can be used for listing and managing courses
    path('courses/manage/', views.manage_courses, name='manage_courses'),  # Optional: can be the same as above
    path('courses/add/', views.manage_courses, name='add_course'),  # Optional: can also be handled in manage_courses
    path('courses/update/<int:pk>/', views.manage_courses, name='update_course'),  # This is handled by the same view
    path('courses/delete/<int:pk>/',views. manage_courses, name='delete_course'),  # This is handled by the same view

     path('manage_teacher/', views.manage_teacher, name='add_teacher'),  # For adding a teacher
    path('manage_teacher/<int:pk>/', views.manage_teacher, name='update_teacher'),  # For updating a teacher
    path('delete_teacher/<int:pk>/', views.delete_teacher, name='delete_teacher'),  # For deleting a teacher
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),  # For listing all teachers

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
