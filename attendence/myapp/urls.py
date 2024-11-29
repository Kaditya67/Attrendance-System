from django.urls import path

from . import studentViews

from . import principalViews

from . import hodViews
from . import views
from . import teacherViews

urlpatterns = [
    path('update_profile/', views.update_student_profile, name='update_student_profile'),
    path('teacher/<int:teacher_id>/update/', teacherViews.update_teacher, name='update_teach'),
    path('students/<int:student_id>/update/', teacherViews.update_student, name='update_student'),

    path('labs/', teacherViews.lab_dashboard, name='lab_dashboard'),
    path('labs/add/', teacherViews.add_lab, name='add_lab'),
    path('labs/<int:lab_id>/add_batches/', teacherViews.add_batches, name='add_batches'),
    path('labs/<int:lab_id>/assign_batches/', teacherViews.assign_batches_to_students, name='assign_batches'),
    path('labs/<int:lab_id>/select_batches/', views.select_batch_and_students, name='select_batches'),
    path('labs/<int:lab_id>/', teacherViews.lab_detail, name='lab_detail'),
    path('batches/<int:batch_id>/delete/', teacherViews.delete_batch, name='delete_batch'),
    #to do
    path('attendance/select/', teacherViews.select_course_lecture, name='select_course_lecture'),
    path('attendance/edit/<int:subject_id>/<str:date>/<int:lecture_number>/', teacherViews.edit_attendance, name='edit_attendance'),
    path('attendance_lab/edit/<int:lab_id>/<str:date>/<int:session_number>/<str:batch>/', teacherViews.edit_lab_attendance, name='edit_lab_attendance'),

    path('update_Attendance',teacherViews.update_Attendance,name='update_Attendance'), 
    path('update_lab_Attendance',teacherViews.update_lab_Attendance,name='update_lab_Attendance'), 
    path('fetch_students/', teacherViews.fetch_students, name='fetch_students'),
    path('fetch_lab_students/', teacherViews.fetch_lab_students, name='fetch_lab_students'),
    path('Add_Attendance',teacherViews.Add_Attendance,name='Add_Attendance'),
    path('Add_Lab_Attendance',teacherViews.Add_Lab_Attendance,name='Add_Lab_Attendance'),
    path('view_Attendance',teacherViews.view_attendance,name='view_Attendance'),
    path('view_lab_Attendance',teacherViews.view_lab_attendance,name='view_lab_Attendance'),
    path('submit_attendance/', teacherViews.submit_attendance, name='submit_attendance'),
    path('submit_lab_attendance/', teacherViews.submit_lab_attendance, name='submit_lab_attendance'),
    # path('SubjectDetails',views.SubjectDetails,name='SubjectDetails'),
    
    path('teacher_dashboard',teacherViews.Subject_Attendance_Details,name='Teacher_dashboard'), 
    path('subject_attendance/', teacherViews.Subject_Attendance_Details, name='subject_attendance'),

    #to do
    path('update_Attendance',views.update_Attendance,name='update_Attendance'), 
    path('fetch_students/', views.fetch_students, name='fetch_students'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('SubjectDetails/<str:student_id>/<int:course_id>/', studentViews.SubjectDetails, name='SubjectDetails'),

    path('StudentDashBoard/<str:student_id>/',studentViews.StudentDashBoard,name='StudentDashBoard'),
    
    path('PrincipalDashboard/',principalViews.PrincipalDashboard,name='PrincipalDashboard'),
    path('HOD_Dashboard',hodViews.HOD_Dashboard,name='HOD_Dashboard'),

    path('attendance-details/<str:year_code>/', studentViews.AttendanceDetailsView.as_view(), name='attendance_details'),
    path('subject_attendance/', views.subject_attendance, name='subject_attendance'),
    path('get-subjects/', views.get_subjects_by_year, name='get_subjects_by_year'),
    path('get_students_by_subject/', hodViews.get_students_by_subject, name='get_students_by_subject'),
    path('add_course/<int:semester_id>/', views.add_course, name='add_course'),
    path('get_subjects_by_year/', views.get_subjects_by_year, name='get_subjects_by_year'), 
    
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
    path('update/student/', studentViews.update_student, name='update_student'),

    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('hod/dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Attendance
    # path('mark_attendance/', views.attendance, name='mark_attendance'),
    
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

    
    path('courses/', views.manage_courses, name='course_list'),  # This can be used for listing and managing courses
    path('courses/manage/', views.manage_courses, name='manage_courses'),  # Optional: can be the same as above
    path('courses/add/', views.manage_courses, name='add_course'),  # Optional: can also be handled in manage_courses
    path('courses/update/<int:pk>/', views.manage_courses, name='update_course'),  # This is handled by the same view
    path('courses/delete/<int:pk>/',views. manage_courses, name='delete_course'),  # This is handled by the same view

    path('manage_teacher/', views.manage_teacher, name='add_teacher'),  # For adding a teacher
    path('manage_teacher/<int:pk>/', views.manage_teacher, name='update_teacher'),  # For updating a teacher
    path('delete_teacher/<int:pk>/', views.delete_teacher, name='delete_teacher'),  # For deleting a teacher
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),  # For listing all teachers

    path('manage_staff/', views.manage_staff, name='add_staff'),  # For adding staff
    path('manage_staff/<int:pk>/', views.manage_staff, name='update_staff'),  # For updating staff
    path('delete_staff/<int:pk>/', views.delete_staff, name='delete_staff'),  # For deleting staff
    path('staff/', views.StaffListView.as_view(), name='staff_list'),  # Staff list view

]
