# View for principal dashboard
from django.shortcuts import render
from django.db.models import Count, Q
from .models import Department, Student, Attendance

from django.shortcuts import render
from .models import Department, Student, Attendance

def PrincipalDashboard(request):
    departments = Department.objects.all()
    department_data = []

    if request.user.groups.filter(name='Principal').exists():
        is_hod = False
        is_principal = True
    elif request.user.groups.filter(name='HOD').exists():
        is_hod = True
        is_principal = False
    else:
        is_hod = False
        is_principal = False

    for department in departments:
        # Get the total number of students in this department
        total_students = Student.objects.filter(semester__session_year__department=department).count()

        # Get all attendance records for students in this department
        attendance_records = Attendance.objects.filter(student__semester__session_year__department=department)

        # Count distinct courses based on attendance records for this department
        total_class_entries = attendance_records.values('course').distinct().count()

        # Calculate total number of classes attended for this department
        total_present = attendance_records.filter(present=True).count()

        # Use the same formula for calculating the total number of classes based on attendance
        if total_students > 0:
            total_classes_score = round((total_class_entries / total_students) * 10)  # Round to the nearest whole number
        else:
            total_classes_score = 0.0

        # Calculate overall attendance percentage for the department
        if attendance_records.count() > 0:  # Only calculate if there are attendance records
            overall_attendance_percentage = (total_present / attendance_records.count()) * 100
        else:
            overall_attendance_percentage = 0.0  # No attendance records, so 0%

        # Append department data to the list for rendering
        department_data.append({
            'name': department.name,  # Department name
            'total_classes': total_classes_score,  # Use the rounded total classes score
            'total_students': total_students,  # Number of students in the department
            'attendance_percentage': round(overall_attendance_percentage, 2),  # Rounded to 2 decimal places
        })

    # Render the PrincipalDashboard template and pass the department data
    return render(request, 'PrincipalDashboard.html', {'department_data': department_data, 'is_hod': is_hod, 'is_principal': is_principal})
