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
from .models import Labs, Batches, Teacher, Student, Course, Attendance, Semester, LabsBatches, Year

from .forms import TeacherUpdateForm
from .forms import (
    StudentRegistrationForm, TeacherRegistrationForm,
    HODRegistrationForm, StaffRegistrationForm,
    PrincipalRegistrationForm, UserLoginForm, AttendanceForm,
    CourseEnrollmentForm,
    AttendanceReportForm,
    StudentUpdateForm  # Only if used in update_student
)
from .models import (
    Student, Teacher, HOD, Staff, Semester, LabsBatches, Attendance, TIME_SLOT_CHOICES, Labs
)

import plotly.graph_objects as go
import plotly.io as pio
from .models import TIME_SLOT_CHOICES  # Only if used in attendance
import json

# View for updating attendance
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher, Attendance, Course
from django.db.models import Max

@login_required
def update_Attendance(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = teacher.assigned_courses.all()

    if request.method == 'POST':

        # Step 1: Fetch attendance records (Subject and Date selection)
        if 'fetch' in request.POST:
            subject_id = request.POST.get('subject')
            date = request.POST.get('date')

            course = get_object_or_404(Course, id=subject_id)
            attendance_records = Attendance.objects.filter(course=course, date=date)

            if not attendance_records.exists():
                messages.warning(request, "No attendance records found for the selected date.")
                return redirect('update_Attendance')

            max_count = attendance_records.aggregate(Max('count'))['count__max']
            lecture_numbers = list(range(1, max_count + 1))

            context = {
                'courses': courses,
                'lecture_numbers': lecture_numbers,
                'selected_course': course,
                'selected_date': date,
            }
            return render(request, 'teachertemplates/Update_Attedance.html', context)

        # Step 3: Update attendance records
        elif 'update_attendance' in request.POST and 'lecture_number' in request.POST:
            subject_id = request.POST.get('subject')
            date = request.POST.get('date')
            lecture_number = request.POST.get('lecture_number')

            course = get_object_or_404(Course, id=subject_id)
            attendance_records = Attendance.objects.filter(course=course, date=date, count=lecture_number)

            attendance_updated = 0
            for record in attendance_records:
                student_id = record.student.id
                attendance_status = request.POST.get(f'attendance_{student_id}', None)

                if attendance_status is not None:
                    record.present = (attendance_status == 'Present')
                    record.save()
                    attendance_updated += 1

            if attendance_updated > 0:
                messages.success(request, f"{attendance_updated} attendance records updated successfully!")
            else:
                messages.warning(request, "No attendance records were updated.")

            context = {
                'courses': courses,
                'attendance_records': attendance_records,
                'selected_course': course,
                'selected_date': date,
                'lecture_number': lecture_number,
            }
            return render(request, 'teachertemplates/Update_Attedance.html', context)
        # Step 2: Load attendance for a specific lecture number
        elif 'lecture_number' in request.POST:
            subject_id = request.POST.get('subject')
            date = request.POST.get('date')
            lecture_number = request.POST.get('lecture_number')

            course = get_object_or_404(Course, id=subject_id)
            attendance_records = Attendance.objects.filter(course=course, date=date, count=lecture_number)

            context = {
                'courses': courses,
                'attendance_records': attendance_records,
                'selected_course': course,
                'selected_date': date,
                'lecture_number': lecture_number,
            }
            return render(request, 'teachertemplates/Update_Attedance.html', context)


    else:
        context = {'courses': courses}
        return render(request, 'teachertemplates/Update_Attedance.html', context)


import plotly.graph_objects as go
import plotly.io as pio
import json
from datetime import datetime

def select_batch_and_students(request, lab_id):
    lab = get_object_or_404(Labs, id=lab_id)
    batch_obj = lab.batches.first()  # Get the first batch object associated with the lab

    # Parse the batch options into a list
    if batch_obj:
        batch_options = json.loads(batch_obj.batch_options)  # Parse JSON string to list
    else:
        batch_options = []

    students = Student.objects.filter(semester=lab.semester)  # Filter students based on lab semester

    if request.method == 'POST':
        selected_batch = request.POST.get('batch')
        student_ids = request.POST.getlist('students')  # Get the list of selected student IDs

        for student_id in student_ids:
            student = get_object_or_404(Student, id=student_id)
            student.assign_batch(lab.index, selected_batch)  # Assign batch based on lab index

        return redirect('some_success_url')  # Redirect after successful assignment

    return render(request, 'select_batch.html', {'lab': lab, 'batch_options': batch_options, 'students': students})


# @login_required
# def update_Attendance(request):
#     if request.method == 'POST':
#         # Logic for updating attendance
#         return HttpResponse("Attendance updated successfully.")
#     else:
#         return render(request, 'teachertemplates/Update_Attedance.html')

# View for adding attendance
from .models import LabsBatches  # Import your LabsBatches model

@login_required
def Add_Attendance(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    
    # Get all courses taught by the teacher
    courses = teacher.assigned_courses.all()

    course_data = []
    for course in courses:
        semester = course.semester
        students_in_semester = Student.objects.filter(semester=semester).distinct()

        course_data.append({
            'course': course,
            'semester': semester,
            'students': students_in_semester,
        })
    
    lab_batches = LabsBatches.objects.all()  # Get all lab batches
    
    context = {
        'course_data': course_data,
        'lab_batches': lab_batches,
    }

    return render(request, 'teachertemplates/add_attendance.html', context)

from django.contrib import messages
from django.shortcuts import redirect
from .models import Attendance, Course, Student


import json

from datetime import datetime

def select_batch_and_students(request, lab_id):
    lab = get_object_or_404(Labs, id=lab_id)
    batch_obj = lab.batches.first()  # Get the first batch object associated with the lab

    # Parse the batch options into a list
    if batch_obj:
        batch_options = json.loads(batch_obj.batch_options)  # Parse JSON string to list
    else:
        batch_options = []

    students = Student.objects.filter(semester=lab.semester)  # Filter students based on lab semester

    if request.method == 'POST':
        selected_batch = request.POST.get('batch')
        student_ids = request.POST.getlist('students')  # Get the list of selected student IDs

        for student_id in student_ids:
            student = get_object_or_404(Student, id=student_id)
            student.assign_batch(lab.index, selected_batch)  # Assign batch based on lab index

        return redirect('some_success_url')  # Redirect after successful assignment

    return render(request, 'select_batch.html', {'lab': lab, 'batch_options': batch_options, 'students': students})





# # View for subject details
# def SubjectDetails(request, student_id, course_id):
#     # Fetch the student using the student_id
#     student = get_object_or_404(Student, student_id=student_id)
    
#     # Fetch the course using the course_id
#     course = get_object_or_404(Course, id=course_id)
    
#     # Retrieve the attendance records for this student and course
#     attendance_records = Attendance.objects.filter(student=student, course=course).order_by('date')
    
#     # Pass the attendance records to the template
#     return render(request, 'SubjectDetails.html', { 
#         'student': student,
#         'course': course,
#         'attendance_records': attendance_records,
#     })



# # View for subject attendance details
@login_required
def Subject_Attendance_Details(request):
    return render(request, 'teachertemplates/Subject_Attedance_Details.html')


# # View for student dashboard
# from django.db.models import Count
# from django.db.models import Avg

# def StudentDashBoard(request, student_id):
#     student = get_object_or_404(Student, student_id=student_id)

#     # Calculate attendance summary, including course ID
#     attendance_summary = Attendance.objects.filter(student=student).values('course__name', 'course__id').annotate(
#         total_classes=Count('id'),
#         attended_classes=Count('id', filter=Q(present=True))
#     )

#     # Prepare attendance data
#     attendance_data = []
#     total_attendance_percentage = 0
#     for record in attendance_summary:
#         total_classes = record['total_classes']
#         attended_classes = record['attended_classes']
#         attendance_percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
#         record['attendance_percentage'] = attendance_percentage
#         total_attendance_percentage += attendance_percentage
#         attendance_data.append(record)

#     # Calculate the average attendance percentage across all courses
#     if len(attendance_data) > 0:
#         average_attendance = total_attendance_percentage / len(attendance_data)
#     else:
#         average_attendance = 0

#     # Calculate missed attendance percentage
#     missed_attendance = 100 - average_attendance

#     return render(request, 'StudentDashBoard.html', {
#         'student': student,
#         'attendance_summary': attendance_data,
#         'average_attendance': average_attendance,  # Pass the average attendance to the template
#         'missed_attendance': missed_attendance,    # Pass the missed attendance to the template
#     })

# from django.shortcuts import render
# from django.db.models import Count, Q
# from .models import Department, Student, Attendance

# from django.shortcuts import render
# from .models import Department, Student, Attendance

# def PrincipalDashboard(request):
#     departments = Department.objects.all()
#     department_data = []

#     for department in departments:
#         # Get the total number of students in this department
#         total_students = Student.objects.filter(semester__session_year__department=department).count()

#         # Get all attendance records for students in this department
#         attendance_records = Attendance.objects.filter(student__semester__session_year__department=department)

#         # Count distinct courses based on attendance records for this department
#         total_class_entries = attendance_records.values('course').distinct().count()

#         # Calculate total number of classes attended for this department
#         total_present = attendance_records.filter(present=True).count()

#         # Use the same formula for calculating the total number of classes based on attendance
#         if total_students > 0:
#             total_classes_score = round((total_class_entries / total_students) * 10)  # Round to the nearest whole number
#         else:
#             total_classes_score = 0.0

#         # Calculate overall attendance percentage for the department
#         if attendance_records.count() > 0:  # Only calculate if there are attendance records
#             overall_attendance_percentage = (total_present / attendance_records.count()) * 100
#         else:
#             overall_attendance_percentage = 0.0  # No attendance records, so 0%

#         # Append department data to the list for rendering
#         department_data.append({
#             'name': department.name,  # Department name
#             'total_classes': total_classes_score,  # Use the rounded total classes score
#             'total_students': total_students,  # Number of students in the department
#             'attendance_percentage': round(overall_attendance_percentage, 2),  # Rounded to 2 decimal places
#         })

#     # Render the PrincipalDashboard template and pass the department data
#     return render(request, 'PrincipalDashboard.html', {'department_data': department_data})


# # View for HOD dashboard
# # views.py

# from django.shortcuts import render
# from .models import Year, Student, Attendance

# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Year, Student, Attendance

# def HOD_Dashboard(request):
#     # Fetch the IT department
#     it_department = Department.objects.get(name='Information Technology')
    
#     # Fetch all years
#     years = Year.objects.all()
#     attendance_data = []

#     for year in years:
#         # Fetch all students in this year who belong to the IT department
#         students = Student.objects.filter(semester__year=year.name, semester__session_year__department=it_department)
#         total_students = students.count()

#         # Calculate overall attendance for this year
#         total_attended_classes = 0
#         total_classes = 0

#         for student in students:
#             # Count total classes and attended classes for each student
#             total_classes += student.attendances.count()  # Total classes for each student
#             total_attended_classes += student.attendances.filter(present=True).count()  # Attended classes

#         # Calculate attendance percentage
#         attendance_percentage = (total_attended_classes / total_classes * 100) if total_classes > 0 else 0

#         attendance_data.append({
#             'code': year.name,
#             'name': year.get_name_display(),
#             'total_students': total_students,
#             'attendance_percentage': attendance_percentage,
#         })

#     return render(request, 'HOD_Dashboard.html', {'attendance_data': attendance_data, 'years': years})



# from django.http import JsonResponse
# from .models import Semester, Course  # Import the necessary models

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404 
# from .models import Semester, Attendance, Student, Department

# def get_subjects_by_year(request):
#     year_code = request.GET.get('year_code')
    
#     # Fetch the IT department
#     it_department = get_object_or_404(Department, name='Information Technology')
    
#     # Fetch all semesters that belong to the selected year
#     semester_objects = Semester.objects.filter(year=year_code)

#     subjects = []
    
#     # Check if any semesters were found
#     if not semester_objects.exists():
#         return JsonResponse({'subjects': [], 'message': 'No semesters found for this year.'})

#     # Fetch all courses related to each semester
#     for semester in semester_objects:
#         for course in semester.courses.all():  # Fetch all courses related to the semester
            
#             # Get total classes and classes attended by students in the IT department
#             total_classes = Attendance.objects.filter(course=course).count()  # Total classes for this course
#             classes_attended = Attendance.objects.filter(course=course, present=True).count()  # Classes attended by students
            
#             # Get total students for the course in the IT department
#             total_students = Student.objects.filter(semester=semester, semester__session_year__department=it_department).count()  # Count of IT students in the current semester
            
#             # Calculate class attended score
#             if total_students > 0:
#                 class_attended_score = (classes_attended / total_students) * 10
#             else:
#                 class_attended_score = 0.0
            
#             # Append the course data with calculated attendance details
#             subjects.append({
#                 'code': course.code,
#                 'name': course.name,
#                 'classes_attended': round(class_attended_score, 2),  # Use the new calculated score
#                 'total_classes': total_classes,
#                 'attendance_percentage': round((classes_attended / total_classes) * 100, 2) if total_classes > 0 else 0.0,  # Round to 2 decimal places
#             })
    
#     return JsonResponse({'subjects': subjects})




# from django.http import JsonResponse
# from .models import Course, Attendance, Student

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from .models import Course, Attendance, Student, Department

# def get_students_by_subject(request):
#     subject_code = request.GET.get('subject_code')

#     try:
#         course = Course.objects.get(code=subject_code)
#     except Course.DoesNotExist:
#         return JsonResponse({'students': [], 'error': 'Course not found'}, status=404)

#     # Fetch the IT department
#     it_department = get_object_or_404(Department, name='Information Technology')

#     # Fetch attendance records for the selected course
#     attendances = Attendance.objects.filter(course=course)

#     # Prepare student data and a set to track unique student IDs
#     student_data = []
#     seen_students = set()  # To track unique students

#     for attendance in attendances:
#         student = attendance.student
        
#         # Ensure the student is in the IT department
#         if student.semester.session_year.department != it_department:
#             continue
        
#         # Use student_id as a string to check uniqueness
#         student_id = str(student.user.id)
        
#         if student_id not in seen_students:
#             seen_students.add(student_id)  # Add student ID to the set

#             total_classes = attendances.filter(student=student).count()
#             attended_classes = attendances.filter(student=student, present=True).count()

#             attendance_status = f'Present ({attended_classes}/{total_classes})' if total_classes > 0 else 'No attendance record'

#             student_data.append({
#                 'name': student.user.username,
#                 'attendance_status': attendance_status,
#                 'student_id': student.student_id  # Include the student_id for linking
#             })

#     return JsonResponse({'students': student_data})




# # views.py

# from django.shortcuts import render, get_object_or_404
# from django.views import View
# from .models import Year, Student, Attendance


# class AttendanceDetailsView(View):
#     def get(self, request, year_code):
#         # Fetch the year based on the year_code (should be 'FE', 'SE', etc.)
#         year = get_object_or_404(Year, name=year_code)
        
#         # Fetch the IT department
#         it_department = get_object_or_404(Department, name='Information Technology')
        
#         # Fetch all students in this year who belong to the IT department
#         students = Student.objects.filter(semester__year=year_code, semester__session_year__department=it_department)
#         student_data = []

#         for student in students:
#             total_classes = student.attendances.count()
#             attended_classes = student.attendances.filter(present=True).count()

#             # Calculate average attendance
#             average_attendance = (attended_classes / total_classes * 100) if total_classes > 0 else 0

#             student_data.append({
#                 'name': student.user.username,
#                 'average_attendance': average_attendance,
#                 'student_id': student.student_id,
#             })

#         context = {
#             'year': year.get_name_display(),
#             'student_data': student_data,
#         }

#         return render(request, 'attendance_details.html', context)


# from django.http import JsonResponse
# from django.shortcuts import render
# from .models import Year, Semester, Course

def subject_attendance(request):
    years = Year.objects.all()
    return render(request, 'subject_attendance.html', {'years': years})

# # def get_subjects_by_year(request):
# #     year_code = request.GET.get('year_code')
# #     semester_objects = Semester.objects.filter(year=year_code)
    
# #     # Fetch all courses for the retrieved semesters
# #     subjects = []
# #     for semester in semester_objects:
# #         subjects.extend(semester.courses.all())  # Fetch all courses related to each semester

# #     # Create a list of course names to return as JSON
# #     subject_names = [{'code': course.code, 'name': course.name} for course in subjects]
# #     return JsonResponse({'subjects': subject_names})


# from django.shortcuts import render, redirect
# from .models import Semester, Course

# def add_course(request, semester_id):
#     semester = Semester.objects.get(id=semester_id)  # Get the semester instance

#     if request.method == 'POST':
#         selected_courses = request.POST.getlist('courses')  # Assuming your form has a multi-select for courses

#         # Clear existing courses if necessary (optional)
#         # semester.courses.clear()  # Uncomment if you want to clear existing courses

#         # Add new courses to the semester
#         for course_id in selected_courses:
#             course = Course.objects.get(id=course_id)
#             semester.courses.add(course)  # This adds the course without removing existing ones

#         return redirect('subject_attendance')  # Redirect after saving

#     courses = Course.objects.all()  # Fetch all courses for the selection dropdown
#     return render(request, 'add_course.html', {'semester': semester, 'courses': courses})






# View for forget password
def forget_password(request):
    if request.method == 'POST':
        # Logic for processing password reset
        return HttpResponse("Password reset link sent.")
    else:
        return render(request, 'forget_password.html')

# View for deleting attendance
def Delete_Attendance(request):
    if request.method == 'POST':
        # Logic for deleting attendance
        return HttpResponse("Attendance deleted successfully.")
    else:
        return render(request, 'delete_attendance.html')

# View for class dashboard
def ClassDashboard(request):
    # Logic for displaying class dashboard
    return render(request, 'ClassDashboard.html')


# User Management Views
def register_user(request, form_class, group_name, template_name, success_redirect):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user_instance = form.save()
            user = user_instance.user
            
            # Add user to the specified group
            user_group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(user_group)
            
            auth_login(request, user)
            messages.success(request, f"{group_name} registered successfully!")
            return redirect(success_redirect)
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # Log the errors to the console
    else:
        form = form_class()

    # Get all semesters to pass to the template
    all_semesters = Semester.objects.all()
    return render(request, template_name, {'form': form, 'semesters': all_semesters})


def register_student(request):
    return register_user(
        request, 
        StudentRegistrationForm, 
        'Student', 
        'register_student.html', 
        'student_dashboard'
    )

def register_teacher(request):
    return register_user(request, TeacherRegistrationForm, 'Teacher', 'register_teacher.html', 'dash_teacher')

def register_hod(request):
    return register_user(request, HODRegistrationForm, 'HOD', 'register_hod.html', 'hod_dashboard')

def register_staff(request):
    return register_user(request, StaffRegistrationForm, 'Staff', 'register_staff.html', 'staff_dashboard')

def register_principal(request):
    return register_user(request, PrincipalRegistrationForm, 'Principal', 'register_principal.html', 'principal_dashboard')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            elif user.groups.filter(name='Principal').exists():
                return redirect('principal_dashboard')
            elif user.groups.filter(name='HOD').exists():
                return redirect('hod_dashboard')
            elif user.groups.filter(name='Teacher').exists():
                return redirect('Teacher_dashboard')
            elif user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
            else:
                return redirect('dashboard')
    else:
        form = UserLoginForm()

    return render(request, 'admin/login.html', {'form': form})

def forget_password(request):
    return render(request, 'admin/forgot_password.html')
def logout_view(request):
    auth_logout(request)
    return redirect('login')


# Dashboard Views
@login_required
def student_dashboard(request):
    # Example attendance data
    attendance = 75  # 75% attendance
    absent = 100 - attendance  # 25% absent

    # Create pie chart using Plotly
    fig = go.Figure(data=[go.Pie(
        labels=['Present', 'Absent'],
        values=[attendance, absent],
        marker=dict(
            colors=['#1a73e8', '#ffcc00'],  # Vibrant colors
            line=dict(color='rgba(0, 0, 0, 0)', width=0)  # No border
        ),
        hoverinfo='label+percent',  # Show label and percent on hover
    )])

    # Update layout for better appearance
    fig.update_layout(
        title_text='Attendance Distribution',
        title_font=dict(size=24, color='#333'),  # Improved title styling
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),  # Remove margins for a cleaner look
        height=400  # Fixed height for consistency
    )

    # Convert the figure to HTML without download options
    graph_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False})

    context = {
        'attendance_chart': graph_html,
        'total_attendance': attendance
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
def principal_dashboard(request):
    if not request.user.groups.filter(name='Principal').exists():
        return redirect('no_permission')

    # Fetch all students for the principal's view
    students = Student.objects.all()
    return render(request, 'principal.html', {'students': students})

@login_required
def hod_dashboard(request):
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')

    hod_profile = get_object_or_404(HOD, user=request.user)
    department = hod_profile.department

    teachers = Teacher.objects.filter(department=department)
    students = Student.objects.filter(department=department)

    return render(request, 'hod_dashboard.html', {'department': department, 'teachers': teachers, 'students': students})

@login_required
def staff_dashboard(request):
    if not request.user.groups.filter(name='Staff').exists():
        return redirect('no_permission')

    staff_profile = get_object_or_404(Staff, user=request.user)
    department = staff_profile.department

    students = Student.objects.filter(department=department)
    return render(request, 'staff_dashboard.html', {'students': students})

@login_required
def view_student_details(request):
    if not request.user.groups.filter(name='Staff').exists():
        return redirect('no_permission')

    staff_profile = get_object_or_404(Staff, user=request.user)
    department = staff_profile.department
    students = Student.objects.filter(department=department)

    return render(request, 'view_student_details.html', {'students': students})

@login_required
def view_teacher_details(request):
    if not request.user.groups.filter(name='Principal').exists():
        return redirect('no_permission')

    teachers = Teacher.objects.all()
    return render(request, 'view_teacher_details.html', {'teachers': teachers})


# Student Management Views
@login_required
def update_student(request):
    student_profile = get_object_or_404(Student, user=request.user)
    print(student_profile)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('student_dashboard')
    else:
        form = StudentUpdateForm(instance=student_profile)

    return render(request, 'update_student.html', {'form': form})

@login_required
def success(request):   
    return render(request, 'success.html')

@login_required
def no_permission(request):
    return render(request, 'no_permission.html')

@login_required
def course_enrollment(request):
    if not request.user.groups.filter(name='Student').exists():
        return redirect('no_permission')

    student_profile = get_object_or_404(Student, user=request.user)
    form = CourseEnrollmentForm(request.POST or None, instance=student_profile)

    if form.is_valid():
        form.save()
        messages.success(request, "Course enrollment updated successfully!")
        return redirect('student_dashboard')

    return render(request, 'course_enrollment.html', {'form': form})

