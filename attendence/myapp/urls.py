from django.urls import path
from . import views
from . import teacherViews

urlpatterns = [

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
    path('SubjectDetails',views.SubjectDetails,name='SubjectDetails'),
    path('teacher_dashboard',teacherViews.Subject_Attendance_Details,name='Teacher_dashboard'),
    path('StudentDashBoard',views.StudentDashBoard,name='StudentDashBoard'),
    path('PrincipalDashboard',views.PrincipalDashboard,name='PrincipalDashboard'),
    path('HOD_Dashboard',views.HOD_Dashboard,name='HOD_Dashboard'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('Delete_Attendance',views.Delete_Attendance,name='Delete_Attendance'),
    path('ClassDashboard',views.ClassDashboard,name='ClassDashboard'),
    path('Class_Report',teacherViews.Class_Report,name='Class_Report'),
    
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
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
