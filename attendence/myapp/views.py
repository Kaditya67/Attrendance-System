from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import timezone

from .forms import (
    StudentRegistrationForm, TeacherRegistrationForm,
    HODRegistrationForm, StaffRegistrationForm,
    PrincipalRegistrationForm, UserLoginForm, AttendanceForm,
    CourseEnrollmentForm, CourseManagementForm,
    AttendanceReportForm, PasswordResetForm,
    StudentUpdateForm  # Only if used in update_student
)
from .models import (
    Student, Teacher, HOD, Staff, Principal, Department, Semester,
    Course, LabsBatches, HonorsMinors, Attendance
)

import plotly.graph_objects as go
import plotly.io as pio
from .models import TIME_SLOT_CHOICES  # Only if used in attendance

# View for updating attendance
def update_Attendance(request):
    if request.method == 'POST':
        # Logic for updating attendance
        return HttpResponse("Attendance updated successfully.")
    else:
        return render(request, 'teachertemplates/Update_Attedance.html')

# View for adding attendance
def Add_Attendance(request):
    if request.method == 'POST':
        # Logic for adding attendance
        return HttpResponse("Attendance added successfully.")
    else:
        return render(request, 'teachertemplates/add_attendance.html')

# View for subject details
def SubjectDetails(request):
    # Logic for displaying subject details
    return render(request, 'SubjectDetails.html')

# View for subject attendance details
def Subject_Attendance_Details(request):
    # Logic for displaying subject attendance details
    return render(request, 'teachertemplates/Subject_Attedance_Details.html')

# View for student dashboard
def StudentDashBoard(request):
    # Logic for displaying student dashboard
    return render(request, 'student_dashboard.html')

# View for principal dashboard
def PrincipalDashboard(request):
    # Logic for displaying principal dashboard
    return render(request, 'principal_dashboard.html')

# View for HOD dashboard
def HOD_Dashboard(request):
    # Logic for displaying HOD dashboard
    return render(request, 'hod_dashboard.html')

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

# View for class report
def Class_Report(request):
    # Logic for generating class report
    return render(request, 'teachertemplates/class_report.html')







@login_required
def attendance(request):
    # Get the logged-in teacher
    teacher = get_object_or_404(Teacher, user=request.user)
    print(f"Logged in teacher: {teacher}")

    # Get all courses taught by the teacher
    courses = teacher.assigned_courses.all()
    print(f"Courses taught by the teacher: {courses}")

    # Check if the teacher has any courses
    if courses.count() == 0:
        return render(request, 'mark_attendance.html', {'error': 'No courses available for this teacher.'})

    # Dictionary to hold courses, their semesters, and students of those semesters
    course_data = []

    # Iterate through each course
    for course in courses:
        semester = course.semester  # Get the semester of the current course
        print(f"Course: {course}, Semester: {semester}")

        # Fetch students from this semester
        students_in_semester = Student.objects.filter(semester=semester).distinct()
        print(f"Students in Semester {semester}: {students_in_semester.count()}")

        # Append the course, semester, and its students to the course_data list
        course_data.append({
            'course': course,
            'semester': semester,
            'students': students_in_semester,
        })

    # Handle POST request (process attendance)
    if request.method == 'POST':
        print("Received POST request, processing attendance...")
        
        # Common fields
        lab_batch_id = request.POST.get('lab_batch')  # Get the selected lab batch
        time_slot = request.POST.get('time_slot')  # Get the selected time slot
        present_all = request.POST.get('present_all')  # Checkbox for marking all present

        for course_info in course_data:
            for student in course_info['students']:
                # Determine attendance status based on checkbox
                attendance_status = 'Present' if present_all else request.POST.get(f'student_{student.id}')

                # Create an Attendance entry
                Attendance.objects.create(
                    student=student,
                    course=course_info['course'],
                    lab_batch=LabsBatches.objects.get(id=lab_batch_id) if lab_batch_id else None,
                    date=timezone.now().date(),  # Current date
                    time_slot=time_slot,  # Time slot from the form
                    present=(attendance_status == 'Present'),  # Convert to boolean
                )
        
        return redirect('success')  # Redirect to attendance list after processing

    # Render the attendance creation template with the course, semester, and students data
    return render(request, 'mark_attendance.html', {
        'teacher': teacher,
        'course_data': course_data,  # Send the course data (with semester and students) to the template
        'time_slots': TIME_SLOT_CHOICES,  # Pass time slots to the template
        'lab_batches': LabsBatches.objects.all(),  # Pass all lab batches to the template
    })



# Update attendance
def update_attendance(request, pk):
    attendance = Attendance.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')  # Redirect after updating
    else:
        form = AttendanceForm(instance=attendance)
    
    return render(request, 'update_attendance.html', {'form': form})



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
                return redirect('teacher_dashboard')
            elif user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
            else:
                return redirect('dashboard')
    else:
        form = UserLoginForm()

    return render(request, 'admin/login.html', {'form': form})

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


# Attendance Views
@login_required
def attendance(request):
    # Get the logged-in teacher
    teacher = get_object_or_404(Teacher, user=request.user)

    # Get all courses taught by the teacher
    courses = teacher.assigned_courses.all()

    # Check if the teacher has any courses
    if courses.count() == 0:
        return render(request, 'mark_attendance.html', {'error': 'No courses available for this teacher.'})

    # Dictionary to hold courses, their semesters, and students of those semesters
    course_data = []

    # Iterate through each course
    for course in courses:
        semester = course.semester  # Get the semester of the current course
        # Fetch students from this semester
        students_in_semester = Student.objects.filter(semester=semester).distinct()
        
        # Append the course, semester, and its students to the course_data list
        course_data.append({
            'course': course,
            'semester': semester,
            'students': students_in_semester,
        })

    # Handle POST request (process attendance)
    if request.method == 'POST':
        lab_batch_id = request.POST.get('lab_batch')  # Get the selected lab batch
        time_slot = request.POST.get('time_slot')  # Get the selected time slot
        present_all = request.POST.get('present_all')  # Checkbox for marking all present

        for course_info in course_data:
            for student in course_info['students']:
                # Determine attendance status based on checkbox
                attendance_status = 'Present' if present_all else request.POST.get(f'student_{student.id}')

                # Create an Attendance entry
                Attendance.objects.create(
                    student=student,
                    course=course_info['course'],
                    lab_batch=LabsBatches.objects.get(id=lab_batch_id) if lab_batch_id else None,
                    date=timezone.now().date(),  # Current date
                    time_slot=time_slot,  # Time slot from the form
                    present=(attendance_status == 'Present'),  # Convert to boolean
                )
        
        return redirect('success')  # Redirect to attendance list after processing

    # Render the attendance creation template with the course, semester, and students data
    return render(request, 'mark_attendance.html', {
        'teacher': teacher,
        'course_data': course_data,  # Send the course data (with semester and students) to the template
        'time_slots': TIME_SLOT_CHOICES,  # Pass time slots to the template
        'lab_batches': LabsBatches.objects.all(),  # Pass all lab batches to the template
    })


@login_required
def update_attendance(request, pk):
    attendance = Attendance.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated successfully.")
            return redirect('attendance_list')  # Redirect to the attendance list
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'update_attendance.html', {'form': form})


@login_required
def attendance_report(request):
    if request.method == 'POST':
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']
            course = form.cleaned_data['course']
            student = form.cleaned_data['student']

            # Query to fetch attendance records
            attendance_records = Attendance.objects.filter(student=student, course=course)

            # Prepare data for display
            attendance_data = {
                'present': attendance_records.filter(present=True).count(),
                'absent': attendance_records.filter(present=False).count(),
                'total': attendance_records.count(),
            }

            return render(request, 'attendance_report.html', {'attendance_data': attendance_data, 'student': student})

    form = AttendanceReportForm()
    return render(request, 'attendance_report.html', {'form': form})

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

