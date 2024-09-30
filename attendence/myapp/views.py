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
    CourseEnrollmentForm,
    AttendanceReportForm,
    StudentUpdateForm  # Only if used in update_student
)
from .models import (
    Student, Teacher, HOD, Staff, Semester, LabsBatches, Attendance, TIME_SLOT_CHOICES, Labs
)

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

# View for subject details
def SubjectDetails(request):
    # Logic for displaying subject details
    return render(request, 'SubjectDetails.html')


# View for student dashboard
def StudentDashBoard(request):
    # Logic for displaying student dashboard
    return render(request, 'StudentDashBoard.html')

# View for principal dashboard
def PrincipalDashboard(request):
    # Logic for displaying principal dashboard
    return render(request, 'PrincipalDashboard.html')

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

