from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from collections import defaultdict
import json
from django.urls import reverse  
from .models import Labs, Batches, Teacher, Student, Course, Attendance, Semester, LabsBatches



# View for subject details
def SubjectDetails(request, student_id, course_id):
    # Fetch the student using the student_id
    student = get_object_or_404(Student, student_id=student_id)
    
    # Fetch the course using the course_id
    course = get_object_or_404(Course, id=course_id)
    
    # Retrieve the attendance records for this student and course
    attendance_records = Attendance.objects.filter(student=student, course=course).order_by('date')
    
    # Pass the attendance records to the template
    return render(request, 'dashboardtemplates/SubjectDetails.html', { 
        'student': student,
        'course': course,
        'attendance_records': attendance_records,
    })





# View for student dashboard
from django.db.models import Count
from django.db.models import Avg

def StudentDashBoard(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    # Calculate attendance summary, including course ID
    attendance_summary = Attendance.objects.filter(student=student).values('course__name', 'course__id').annotate(
        total_classes=Count('id'),
        attended_classes=Count('id', filter=Q(present=True))
    )

    # Prepare attendance data
    attendance_data = []
    total_attendance_percentage = 0
    for record in attendance_summary:
        total_classes = record['total_classes']
        attended_classes = record['attended_classes']
        attendance_percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
        record['attendance_percentage'] = attendance_percentage
        total_attendance_percentage += attendance_percentage
        attendance_data.append(record)

    # Calculate the average attendance percentage across all courses
    if len(attendance_data) > 0:
        average_attendance = total_attendance_percentage / len(attendance_data)
    else:
        average_attendance = 0

    # Calculate missed attendance percentage
    missed_attendance = 100 - average_attendance

    return render(request, 'dashboardtemplates/StudentDashBoard.html', {
        'student': student,
        'attendance_summary': attendance_data,
        'average_attendance': average_attendance,  # Pass the average attendance to the template
        'missed_attendance': missed_attendance,    # Pass the missed attendance to the template
    })

from django.shortcuts import render
from django.db.models import Count, Q
from .models import Department, Student, Attendance

from django.shortcuts import render
from .models import Department, Student, Attendance

def PrincipalDashboard(request):
    departments = Department.objects.all()
    department_data = []

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
    return render(request, 'dashboardtemplates/PrincipalDashboard.html', {'department_data': department_data})


# View for HOD dashboard
# views.py

from django.shortcuts import render
from .models import Year, Student, Attendance

from django.shortcuts import render
from django.http import JsonResponse
from .models import Year, Student, Attendance

def HOD_Dashboard(request):
    # Fetch the IT department
    it_department = Department.objects.get(name='Information Technology')
    
    # Fetch all years
    years = Year.objects.all()
    attendance_data = []

    for year in years:
        # Fetch all students in this year who belong to the IT department
        students = Student.objects.filter(semester__year=year.name, semester__session_year__department=it_department)
        total_students = students.count()

        # Calculate overall attendance for this year
        total_attended_classes = 0
        total_classes = 0

        for student in students:
            # Count total classes and attended classes for each student
            total_classes += student.attendances.count()  # Total classes for each student
            total_attended_classes += student.attendances.filter(present=True).count()  # Attended classes

        # Calculate attendance percentage
        attendance_percentage = (total_attended_classes / total_classes * 100) if total_classes > 0 else 0

        attendance_data.append({
            'code': year.name,
            'name': year.get_name_display(),
            'total_students': total_students,
            'attendance_percentage': attendance_percentage,
        })

    return render(request, 'dashboardtemplates/hod_dashboard.html', {'attendance_data': attendance_data, 'years': years})



from django.http import JsonResponse
from .models import Semester, Course  # Import the necessary models

from django.http import JsonResponse
from django.shortcuts import get_object_or_404 
from .models import Semester, Attendance, Student, Department

def get_subjects_by_year(request):
    year_code = request.GET.get('year_code')
    
    # Fetch the IT department
    it_department = get_object_or_404(Department, name='Information Technology')
    
    # Fetch all semesters that belong to the selected year
    semester_objects = Semester.objects.filter(year=year_code)

    subjects = []
    
    # Check if any semesters were found
    if not semester_objects.exists():
        return JsonResponse({'subjects': [], 'message': 'No semesters found for this year.'})

    # Fetch all courses related to each semester
    for semester in semester_objects:
        for course in semester.courses.all():  # Fetch all courses related to the semester
            
            # Get total classes and classes attended by students in the IT department
            total_classes = Attendance.objects.filter(course=course).count()  # Total classes for this course
            classes_attended = Attendance.objects.filter(course=course, present=True).count()  # Classes attended by students
            
            # Get total students for the course in the IT department
            total_students = Student.objects.filter(semester=semester, semester__session_year__department=it_department).count()  # Count of IT students in the current semester
            
            # Calculate class attended score
            if total_students > 0:
                class_attended_score = (classes_attended / total_students) * 10
            else:
                class_attended_score = 0.0
            
            # Append the course data with calculated attendance details
            subjects.append({
                'code': course.code,
                'name': course.name,
                'classes_attended': round(class_attended_score, 2),  # Use the new calculated score
                'total_classes': total_classes,
                'attendance_percentage': round((classes_attended / total_classes) * 100, 2) if total_classes > 0 else 0.0,  # Round to 2 decimal places
            })
    
    return JsonResponse({'subjects': subjects})




from django.http import JsonResponse
from .models import Course, Attendance, Student

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Course, Attendance, Student, Department

def get_students_by_subject(request):
    subject_code = request.GET.get('subject_code')

    try:
        course = Course.objects.get(code=subject_code)
    except Course.DoesNotExist:
        return JsonResponse({'students': [], 'error': 'Course not found'}, status=404)

    # Fetch the IT department
    it_department = get_object_or_404(Department, name='Information Technology')

    # Fetch attendance records for the selected course
    attendances = Attendance.objects.filter(course=course)

    # Prepare student data and a set to track unique student IDs
    student_data = []
    seen_students = set()  # To track unique students

    for attendance in attendances:
        student = attendance.student
        
        # Ensure the student is in the IT department
        if student.semester.session_year.department != it_department:
            continue
        
        # Use student_id as a string to check uniqueness
        student_id = str(student.user.id)
        
        if student_id not in seen_students:
            seen_students.add(student_id)  # Add student ID to the set

            total_classes = attendances.filter(student=student).count()
            attended_classes = attendances.filter(student=student, present=True).count()

            attendance_status = f'Present ({attended_classes}/{total_classes})' if total_classes > 0 else 'No attendance record'

            student_data.append({
                'name': student.user.username,
                'attendance_status': attendance_status,
                'student_id': student.student_id  # Include the student_id for linking
            })

    return JsonResponse({'students': student_data})




# views.py

from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Year, Student, Attendance


class AttendanceDetailsView(View):
    def get(self, request, year_code):
        # Fetch the year based on the year_code (should be 'FE', 'SE', etc.)
        year = get_object_or_404(Year, name=year_code)
        
        # Fetch the IT department
        it_department = get_object_or_404(Department, name='Information Technology')
        
        # Fetch all students in this year who belong to the IT department
        students = Student.objects.filter(semester__year=year_code, semester__session_year__department=it_department)
        student_data = []

        for student in students:
            total_classes = student.attendances.count()
            attended_classes = student.attendances.filter(present=True).count()

            # Calculate average attendance
            average_attendance = (attended_classes / total_classes * 100) if total_classes > 0 else 0

            student_data.append({
                'name': student.user.username,
                'average_attendance': average_attendance,
                'student_id': student.student_id,
            })

        context = {
            'year': year.get_name_display(),
            'student_data': student_data,
        }

        return render(request, 'dashboardtemplates/attendance_details.html', context)



def add_course(request, semester_id):
    semester = Semester.objects.get(id=semester_id)  # Get the semester instance

    if request.method == 'POST':
        selected_courses = request.POST.getlist('courses')  # Assuming your form has a multi-select for courses

        # Clear existing courses if necessary (optional)
        # semester.courses.clear()  # Uncomment if you want to clear existing courses

        # Add new courses to the semester
        for course_id in selected_courses:
            course = Course.objects.get(id=course_id)
            semester.courses.add(course)  # This adds the course without removing existing ones

        return redirect('subject_attendance')  # Redirect after saving

    courses = Course.objects.all()  # Fetch all courses for the selection dropdown
    return render(request, 'add_course.html', {'semester': semester, 'courses': courses})


def super_admin(request):
    return render(request,'dashboardtemplates/super_admin.html')




