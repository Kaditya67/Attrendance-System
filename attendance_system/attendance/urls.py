from django.urls import path
from . import dashboardViews  # Import your views module

urlpatterns = [
    #For dashboard urls
        # HOD Dashboard
        path('hod_dashboard/', dashboardViews.HOD_Dashboard, name='hod_dashboard'),
        path('get_subjects_by_year/', dashboardViews.get_subjects_by_year, name='get_subjects_by_year'),
        path('get_students_by_subject/', dashboardViews.get_students_by_subject, name='get_students_by_subject'),
        
        # Student Dashboard
        path('student_dashboard/<int:student_id>/', dashboardViews.StudentDashBoard, name='student_dashboard'),
        path('subject_details/<int:student_id>/<int:course_id>/', dashboardViews.SubjectDetails, name='subject_details'),

        # Attendance Details
        path('attendance_details/<str:year_code>/', dashboardViews.AttendanceDetailsView.as_view(), name='attendance_details'),

        # Principal Dashboard
        path('principal_dashboard/', dashboardViews.PrincipalDashboard, name='principal_dashboard'),

        # Super Admin Dashboard
        path('super_admin/', dashboardViews.super_admin, name='super_admin'),

        # Example for commented function (if you plan to use it later)
        # path('add_course/<int:semester_id>/', dashboardViews.add_course, name='add_course'),
        
    #--------------------------------------------------------------------------------------------------------------#
]
