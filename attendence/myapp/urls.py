from django.urls import path

from . import dashboardViews
from . import views
from . import teacherViews

from django.urls import path
from . import views



urlpatterns = [


    path('super_admin/',dashboardViews.super_admin,name='super_admin'),
    path('teacher/<int:teacher_id>/update/', teacherViews.update_teacher, name='update_teacher'),

    path('labs/', teacherViews.lab_dashboard, name='lab_dashboard'),
    path('labs/<int:lab_id>/add_batches/', teacherViews.add_batches, name='add_batches'),
    path('labs/<int:lab_id>/assign_batches/', teacherViews.assign_batches_to_students, name='assign_batches'),
    path('labs/<int:lab_id>/select_batches/', views.select_batch_and_students, name='select_batches'),
    path('labs/<int:lab_id>/', teacherViews.lab_detail, name='lab_detail'),
    path('batches/<int:batch_id>/delete/', teacherViews.delete_batch, name='delete_batch'),
    #to do
    path('attendance/select/', teacherViews.select_course_lecture, name='select_course_lecture'),
    path('attendance/edit/<int:subject_id>/<str:date>/<int:lecture_number>/', teacherViews.edit_attendance, name='edit_attendance'),

    path('update_Attendance',teacherViews.update_Attendance,name='update_Attendance'), 
    path('fetch_students/', teacherViews.fetch_students, name='fetch_students'),
    path('Add_Attendance',teacherViews.Add_Attendance,name='Add_Attendance'),
    path('view_Attendance',teacherViews.view_attendance,name='view_Attendance'),
    path('submit_attendance/', teacherViews.submit_attendance, name='submit_attendance'),
    path('SubjectDetails',dashboardViews.SubjectDetails,name='SubjectDetails'),
    
    path('teacher_dashboard',teacherViews.Subject_Attendance_Details,name='Teacher_dashboard'),

    #to do
    path('update_Attendance',views.update_Attendance,name='update_Attendance'), 
    path('fetch_students/', views.fetch_students, name='fetch_students'),
    path('Add_Attendance',views.Add_Attendance,name='Add_Attendance'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('SubjectDetails/<str:student_id>/<int:course_id>/', dashboardViews.SubjectDetails, name='SubjectDetails'),

    path('StudentDashBoard/<str:student_id>/',dashboardViews.StudentDashBoard,name='StudentDashBoard'),
    
    path('PrincipalDashboard',dashboardViews.PrincipalDashboard,name='PrincipalDashboard'),
    path('HOD_Dashboard',dashboardViews.HOD_Dashboard,name='HOD_Dashboard'),


    path('attendance-details/<str:year_code>/', dashboardViews.AttendanceDetailsView.as_view(), name='attendance_details'),
    path('subject_attendance/', views.subject_attendance, name='subject_attendance'),
    path('get-subjects/', dashboardViews.get_subjects_by_year, name='get_subjects_by_year'),
    path('get_students_by_subject/', dashboardViews.get_students_by_subject, name='get_students_by_subject'),
    path('add_course/<int:semester_id>/', dashboardViews.add_course, name='add_course'),
    path('get_subjects_by_year/', dashboardViews.get_subjects_by_year, name='get_subjects_by_year'), 
    
    path('forget_password',views.forget_password,name='forget_password'),
    
    path('Delete_Attendance',views.Delete_Attendance,name='Delete_Attendance'),
    path('ClassDashboard',views.ClassDashboard,name='ClassDashboard'),
    path('Class_Report',teacherViews.Class_Report,name='Class_Report'),
    path('Class_Report',teacherViews.Class_Report,name='Class_Report'),
    
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('forget_password/', views.forget_password, name='forget_password'),
    
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

    path('course/enrollment/', views.course_enrollment, name='course_enrollment'),

    path('view/student/details/', views.view_student_details, name='view_student_details'),
    path('view/teacher/details/', views.view_teacher_details, name='view_teacher_details'),
    
    # Miscellaneous
    path('success/', views.success, name='success'),
    path('no_permission/', views.no_permission, name='no_permission'),
]
