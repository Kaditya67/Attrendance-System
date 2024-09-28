from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import (StudentRegistrationForm, TeacherRegistrationForm,
                    HODRegistrationForm, StaffRegistrationForm,
                    PrincipalRegistrationForm, UserLoginForm, AttendanceForm,
                    CourseEnrollmentForm, CourseManagementForm, LectureSchedulingForm, 
                    AttendanceReportForm, 
                    # StudentProfileUpdateForm, 
                    PasswordResetForm)
from .models import (Student, Teacher, HOD, Staff, Principal, Department, Semester,
                     HonorsMinors, Course, Attendance)
from django.db.models import Q
import plotly.graph_objects as go
import plotly.io as pio
import base64
import io
from django.shortcuts import render


from django.shortcuts import render, redirect

from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from .models import Student

def student_form(request):
    # Fetch all student records from the database
    students = Student.objects.all()

    if request.method == 'POST':
        # Process attendance for each student
        for student in students:
            attendance_status = request.POST.get(f'attendance_{student.id}', 'absent')
            # Here you can replace the logic to save the attendance in the database.
            # For example:
            # Attendance.objects.create(student=student, status=attendance_status)
            print(f"Student {student.user.first_name} ({student.roll_number}): {attendance_status}")

        return redirect('student_form')  # Redirect to the form after submission

    # Render the student form with the list of students
    return render(request, 'student_form.html', {'students': students})


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

from datetime import datetime

def get_current_time_slot():
    now = datetime.now()
    current_time = now.strftime('%H:%M')  # Get current time in 24-hour format

    # Define time slots with start and end times for easy comparison
    time_slots = {
        '8-9': ('08:00', '09:00'),
        '9-10': ('09:00', '10:00'),
        '10-11': ('10:00', '11:00'),
        '11:15-12:15': ('11:15', '12:15'),
        '12:15-1:15': ('12:15', '13:15'),  # 1:15 PM in 24-hour format is 13:15
        '2-3': ('14:00', '15:00'),
        '3-4': ('15:00', '16:00'),
        '4-5': ('16:00', '17:00'),
    }

    # Check which time slot the current time falls into
    for slot, (start, end) in time_slots.items():
        if start <= current_time < end:
            return slot  # Return the slot if current time falls within its range

    return None  # No matching time slot

def get_teacher_courses(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    # Get all courses assigned to the teacher
    courses = teacher.assigned_courses.all()

    course_data = []
    for course in courses:
        semester = course.semester  # Assuming course has a semester field
        students_in_semester = Student.objects.filter(semester=semester).distinct()  # Fetch distinct students for the semester

        # Append course, semester, and students information to course_data
        course_data.append({
            'course': course,
            'semester': semester,
            'students': students_in_semester,
        })

    return course_data

@login_required
def fetch_students(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')

        # Get the selected course
        course = Course.objects.get(id=subject_id)
        semester = course.semester

        # Get students for the selected course's semester
        students = Student.objects.filter(semester=semester)

        context = {
            'students': students,
            'selected_course': course,
            'selected_date': date,
            'course_data': get_teacher_courses(request),  # Function to fetch teacher's courses
        }

        return render(request, 'teachertemplates/add_attendance.html', context)
    
    return redirect('Add_Attendance')


# def Submit_Attendance(request):
#     if request.method == "POST":
#         subject_id = request.POST.get('subject')
#         date = request.POST.get('date')
#         lab_batch_id = request.POST.get('lab_batch') or None  # Set to None if empty
#         common_notes = request.POST.get('common_notes', '')  # Default to empty string if not provided
#         absent_students = request.POST.get('absent_students', '').split(',')  # Get absent student IDs

#         course = Course.objects.get(id=subject_id)
#         time_slot = get_current_time_slot()  # Automatically determine the time slot
        
#         attendance_created = 0  # To track how many records were created

#         print(f'Course: {course}, Date: {date}, Lab Batch ID: {lab_batch_id}, Common Notes: {common_notes}, subject_id: {subject_id}')


#         for key in request.POST:
#             if key.startswith('attendance_'):
#                 student_id = key.split('_')[1]  # Extract student ID from key
#                 attendance_status = request.POST[key]  # Get the attendance status

#                 print(f'Processing student_id: {student_id}, attendance_status: {attendance_status}')  # Log student ID and status

#                 student = Student.objects.get(id=int(student_id))
#                 present = (attendance_status == 'Present')  # Check if status is 'Present'

#                 # Create or update attendance record
#                 attendance_record, created = Attendance.objects.update_or_create(
#                     student=student,
#                     course=course,
#                     date=date,
#                     time_slot=time_slot,
#                     defaults={
#                         'lab_batch_id': lab_batch_id,
#                         'present': present,
#                         'notes': common_notes,  # Store common notes
#                     }
#                 )
                
#                 attendance_created += 1  # Count the number of created or updated records

#         # Now create records for absent students
#         for student_id in absent_students:
#             if student_id:  # Ensure student_id is not empty
#                 student = Student.objects.get(id=int(student_id))
#                 # Create absence record
#                 Attendance.objects.update_or_create(
#                     student=student,
#                     course=course,
#                     date=date,
#                     defaults={
#                         'lab_batch_id': lab_batch_id,
#                         'present': False,  # Mark as absent
#                         'notes': common_notes,
#                     }
#                 )
#                 attendance_created += 1  # Count the absent record

#         # Provide feedback based on the outcome
#         if attendance_created > 0:
#             messages.success(request, f"{attendance_created} attendance records submitted successfully!")
#         else:
#             messages.warning(request, "No attendance records were created.")

#         return redirect('Add_Attendance')

#     return redirect('Add_Attendance')

@login_required
def submit_attendance(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        common_notes = request.POST.get('common_notes', '')
        absent_students = request.POST.get('absent_students', '').split(',')

        course = Course.objects.get(id=subject_id)

        # Retrieve current attendance records
        existing_attendance_records = Attendance.objects.filter(course=course, date=date)
        common_count = existing_attendance_records.last().count + 1 if existing_attendance_records.exists() else 1

        attendance_created = 0

        for key in request.POST:
            if key.startswith('attendance_'):
                student_id = key.split('_')[1]
                student = Student.objects.get(id=int(student_id))
                present = request.POST[key] == 'Present'

                Attendance.objects.create(
                    student=student,
                    course=course,
                    date=date,
                    present=present,
                    count=common_count,
                    notes=common_notes
                )
                attendance_created += 1

        for student_id in absent_students:
            if student_id:
                student = Student.objects.get(id=int(student_id))
                Attendance.objects.create(
                    student=student,
                    course=course,
                    date=date,
                    present=False,
                    count=common_count,
                    notes=common_notes
                )
                attendance_created += 1

        if attendance_created > 0:
            messages.success(request, f"{attendance_created} attendance records submitted successfully!")
        else:
            messages.warning(request, "No attendance records were created.")

        return redirect('Add_Attendance')

    return redirect('Add_Attendance')



# View for subject details
def SubjectDetails(request):
    # Logic for displaying subject details
    return render(request, 'SubjectDetails.html')

# View for subject attendance details
@login_required
def Subject_Attendance_Details(request):
    return render(request, 'teachertemplates/Subject_Attedance_Details.html')

# View for student dashboard
from django.db.models import Count
def StudentDashBoard(request,student_id):
    
    student = get_object_or_404(Student, student_id=student_id)

    attendance_summary = Attendance.objects.filter(student=student).values('course__name').annotate(
        total_classes=Count('id'),
        attended_classes=Count('id', filter=Q(present=True))
    )
    # Fetch other necessary data for the attendance records if needed
    attendance_data = []
    for record in attendance_summary:
        total_classes = record['total_classes']
        attended_classes = record['attended_classes']
        attendance_percentage = (attended_classes / total_classes * 100) if total_classes > 0 else 0
        record['attendance_percentage'] = attendance_percentage
        attendance_data.append(record)

    return render(request, 'StudentDashBoard.html', {
        'student': student,
        'attendance_summary': attendance_summary,
    })
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

# View for class report
@login_required
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


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentUpdateForm

@login_required
def update_student(request):
    if not request.user.groups.filter(name='Student').exists():
        return redirect('no_permission')
    student = request.user.student  # Assuming a OneToOne relation with User
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Your details have been updated successfully.")
            return redirect('student_dashboard')
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, 'update_student.html', {'form': form, 'student': student})



@login_required
def success(request):   
    return render(request, 'success.html')

@login_required
def dashboard_view(request, role_name, template_name):
    if not request.user.groups.filter(name=role_name).exists():
        return redirect('no_permission')

    profile_model = {
        'Teacher': Teacher,
        'HOD': HOD,
        'Staff': Staff,
        'Student': Student
    }.get(role_name)

    if not profile_model:
        return redirect('no_permission')

    profile = profile_model.objects.get(user=request.user)
    department = getattr(profile, 'department', None)
    context = {
        'department': department,
        'teachers': Teacher.objects.filter(department=department) if department else None,
        'students': Student.objects.filter(department=department) if department else None,
        'courses': getattr(profile, 'courses', None)
    }

    return render(request, template_name, context)

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
                return redirect('dash_teacher')
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

@login_required
def mark_attendance(request):
    courses = Course.objects.none()
    
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect('no_permission')

    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == 'POST':
        form = AttendanceForm(request.POST, teacher_courses=teacher.courses_taught.all())
        if form.is_valid():
            course = form.cleaned_data.get('course')
            students = Student.objects.filter(courses=course)

            for student in students:
                attendance_status = request.POST.get(f'student_{student.id}')
                if attendance_status:
                    Attendance.objects.update_or_create(
                        student=student,
                        course=course,
                        date=form.cleaned_data.get('date'),
                        defaults={'status': attendance_status, 'teacher': teacher}
                    )
                    
            messages.success(request, "Attendance successfully marked.")
            return redirect('success')
        else:
            messages.error(request, "There was an error in the form. Please check your input.")
    else:
        courses = teacher.courses_taught.all()
        form = AttendanceForm(teacher_courses=courses)

    return render(request, 'mark_attendance.html', {'form': form, 'courses': courses})

@login_required
def no_permission(request):
    return render(request, 'no_permission.html')

@login_required
def view_grades(request):
    
    if not request.user.groups.filter(name='Student').exists():
        return redirect('no_permission')

    student_profile = get_object_or_404(Student, user=request.user)
    grades = student_profile.grades.all()  # Assuming Student has related grades

    return render(request, 'view_grades.html', {'grades': grades})

@login_required
def principal_view(request):
    department_id = request.GET.get('department', '')
    semester_id = request.GET.get('semester', '')
    honors_minors_id = request.GET.get('honors_minors', '')
    status = request.GET.get('status', '')
    search_query = request.GET.get('search', '')

    students = Student.objects.all()

    if department_id:
        students = students.filter(department_id=department_id)

    if semester_id:
        students = students.filter(
            Q(even_sem__id=semester_id) | Q(odd_sem__id=semester_id)
        )

    if honors_minors_id:
        students = students.filter(honors_minors_id=honors_minors_id)

    if status:
        students = students.filter(status=status)

    if search_query:
        students = students.filter(
            Q(user__username__icontains=search_query) | 
            Q(user__first_name__icontains=search_query) | 
            Q(user__last_name__icontains=search_query)
        )

    departments = Department.objects.all()
    all_semesters = Semester.objects.all()
    honors_minors = HonorsMinors.objects.all()
    statuses = Student.objects.values_list('status', flat=True).distinct()

    context = {
        'students': students,
        'departments': departments,
        'all_semesters': all_semesters,
        'honors_minors': honors_minors,
        'statuses': statuses
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'student_table_rows.html', context)

    return render(request, 'principal.html', context)

def index(request):
    return render(request, 'index.html')


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
def view_teacher_details(request):
    if not request.user.groups.filter(name='Principal').exists():
        return redirect('no_permission')

    teachers = Teacher.objects.all()
    return render(request, 'view_teacher_details.html', {'teachers': teachers})

@login_required
def hod_dashboard(request):
    return render(request,'hod_dashboard.html')

@login_required
def manage_teachers(request):
    if not (request.user.groups.filter(name='HOD').exists() or request.user.groups.filter(name='Principal').exists()):
        return render(request, 'principal.html', {'students': students})

@login_required
def hod_dashboard(request):
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')

    hod_profile = get_object_or_404(HOD, user=request.user)
    department = hod_profile.department
    teachers = Teacher.objects.filter(department=department)

    return render(request, 'manage_teachers.html', {'teachers': teachers})

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
def student_dashboard(request):
    # Example attendance data
    attendance = 75  # 75% attendance
    absent = 100 - attendance  # 25% absent

    # Create pie chart using Plotly
    fig = go.Figure(data=[go.Pie(
        labels=['Present', 'Absent'],
        values=[attendance, absent],
        marker=dict(
            colors=['AABD8C', '#D3C99E'],  # Vibrant colors
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

@login_required
def course_management(request):
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')

    form = CourseManagementForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Course managed successfully!")
        return redirect('hod_dashboard')

    return render(request, 'course_management.html', {'form': form})

@login_required
def lecture_scheduling(request):
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')

    form = LectureSchedulingForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Lecture scheduled successfully!")
        return redirect('hod_dashboard')

    return render(request, 'lecture_scheduling.html', {'form': form})

@login_required
def attendance_reporting(request):
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')

    form = AttendanceReportForm(request.POST or None)

    if form.is_valid():
        report = form.generate_report()
        messages.success(request, "Attendance report generated successfully!")
        return render(request, 'attendance_report.html', {'report': report})

    return render(request, 'attendance_reporting.html', {'form': form})

# @login_required
# def profile_update(request):
#     form = StudentProfileUpdateForm(request.POST or None, instance=request.user.profile)

#     if form.is_valid():
#         form.save()
#         messages.success(request, "Profile updated successfully!")
#         return redirect('dashboard')

#     return render(request, 'profile_update.html', {'form': form})

@login_required
def password_reset(request):
    form = PasswordResetForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Password reset successful!")
        return redirect('login')

    return render(request, 'password_reset.html', {'form': form})

def dashboard(request):
    department = request.user.department if hasattr(request.user, 'department') else None
    teachers = department.teacher_set.all() if department else None
    students = department.student_set.all() if department else None
    courses = request.user.courses.all() if hasattr(request.user, 'courses') else None

    is_teacher = request.user.groups.filter(name="Teacher").exists()
    is_hod = request.user.groups.filter(name="HOD").exists()
    is_staff = request.user.groups.filter(name="Staff").exists()
    is_student = request.user.groups.filter(name="Student").exists()

    context = {
        'department': department,
        'teachers': teachers,
        'students': students,
        'courses': courses,
        'is_teacher': is_teacher,
        'is_hod': is_hod,
        'is_staff': is_staff,
        'is_student': is_student,
    }

    return render(request, 'dashboard.html', context)

@login_required
def dash_teacher(request):
    return render(request, 'dash_teacher.html')

def demo_dash(request):
    return render(request, 'demo_dash.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
# from .forms import StudentForm

# Add Student View
# def add_student(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('view_student_details')
#     else:
#         form = StudentForm()
#     return render(request, 'add_edit_student.html', {'form': form, 'action': 'Add'})

# # Edit Student View
# def edit_student(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
#     if request.method == 'POST':
#         form = StudentForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             return redirect('view_student_details')
#     else:
#         form = StudentForm(instance=student)
#     return render(request, 'add_edit_student.html', {'form': form, 'action': 'Edit'})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm

# Add Course View
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm()
    return render(request, 'add_edit_course.html', {'form': form, 'action': 'Add'})

# Edit Course View
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'add_edit_course.html', {'form': form, 'action': 'Edit'})

from django.shortcuts import render, redirect
from .models import Lecture
from .forms import LectureForm

# Schedule Lecture View
def schedule_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_lectures')
    else:
        form = LectureForm()
    return render(request, 'schedule_lecture.html', {'form': form})



from django.shortcuts import render
from .models import Attendance

# View Attendance Report
def view_attendance_report(request):
    reports = Attendance.objects.all()  # Modify as needed for your reporting logic
    return render(request, 'attendance_report.html', {'reports': reports})



# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import login as auth_login, logout as auth_logout
# from django.contrib.auth.models import Group
# from .forms import (StudentRegistrationForm, TeacherRegistrationForm, 
#                     HODRegistrationForm, StaffRegistrationForm, 
#                     PrincipalRegistrationForm, UserLoginForm, AttendanceForm)
# from .models import (Student, Teacher, HOD, Staff, Principal, Department, 
#                      EvenSem, OddSem, HonorsMinors)
# from django.contrib.auth.decorators import login_required

# def register_student(request):
#     if request.method == "POST":
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the new student and user
#             student = form.save()
            
#             # Add the user to the "Student" group
#             user = student.user
#             student_group, created = Group.objects.get_or_create(name='Student')
#             user.groups.add(student_group)
            
#             # Optionally, you can also add the user to the group using:
#             # student.user.groups.add(Group.objects.get(name='Student'))

#             messages.success(request, "Student registered successfully!")
#             return redirect('student_dashboard')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = StudentRegistrationForm()

#     return render(request, 'register_student.html', {'form': form})
# # views.py

# def register_teacher(request):
#     if request.method == 'POST':
#         form = TeacherRegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the new teacher and user
#             teacher = form.save()
            
#             # Add the user to the "Teachers" group
#             user = teacher.user
#             teachers_group, created = Group.objects.get_or_create(name='Teacher')
#             user.groups.add(teachers_group)
            
#             messages.success(request, "Teacher registered successfully!")
#             return redirect('dash_teacher')  # Redirect to a success page or wherever you want
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = TeacherRegistrationForm()

#     return render(request, 'teacher_register.html', {'form': form})



# # myapp/views.py

# def register_hod(request):
#     if request.method == 'POST':
#         form = HODRegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the new HOD and user
#             hod = form.save()
            
#             # Add the user to the "HODs" group
#             user = hod.user
#             hods_group, created = Group.objects.get_or_create(name='HOD')
#             user.groups.add(hods_group)
            
#             messages.success(request, "HOD registered successfully!")
#             return redirect('hod_dashboard')  # Replace with your success URL
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = HODRegistrationForm()

#     return render(request, 'register_hod.html', {'form': form})


# def register_staff(request):
#     if request.method == 'POST':
#         form = StaffRegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the new staff user
#             user = form.save()

#             # Add the user to the "Staff" group
#             staff_group, created = Group.objects.get_or_create(name='Staff')
#             user.groups.add(staff_group)

#             # Optionally log in the new staff member
#             # auth_login(request, user)  # Uncomment if you want to log them in automatically

#             messages.success(request, "Staff registered successfully!")
#             return redirect('staff_dashboard')  # Replace with your actual success URL
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = StaffRegistrationForm()

#     return render(request, 'register_staff.html', {'form': form})

# def register_principal(request):
#     if request.method == 'POST':
#         form = PrincipalRegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the new Principal and user
#             user = form.save()

#             # Add the user to the "Principals" group
#             principals_group, created = Group.objects.get_or_create(name='Principal')
#             user.groups.add(principals_group)

#             # Optionally log in the new principal
#             auth_login(request, user)

#             messages.success(request, "Principal registered successfully!")
#             return redirect('principal_dashboard')  # Replace with your success URL
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = PrincipalRegistrationForm()

#     return render(request, 'register_principal.html', {'form': form})

# @login_required
# def success(request):   
#     return render(request, 'success.html')

    
# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)
            
#             # Redirect based on user role/type
#             if user.is_superuser:
#                 return redirect('/admin/')  # Redirect superuser/admin to their dashboard
#             elif user.groups.filter(name='Principal').exists():
#                 return redirect('principal_dashboard')  # Redirect Principal
#             elif user.groups.filter(name='HOD').exists():
#                 return redirect('hod_dashboard')  # Redirect HOD
#             elif user.groups.filter(name='Teacher').exists():
#                 return redirect('teacher_dashboard')  # Redirect Teacher
#             elif user.groups.filter(name='Student').exists():
#                 return redirect('student_dashboard')  # Redirect Student
#             else:
#                 return redirect('dashboard')  # Default dashboard if no group is found
#     else:
#         form = UserLoginForm()
    
#     return render(request, 'login.html', {'form': form})

# def logout_view(request):
#     auth_logout(request)
#     return redirect('login')

    
# @login_required
# def mark_attendance(request):
#     if not request.user.groups.filter(name='Teacher').exists():
#         return redirect('no_permission')  # Redirect to a page showing no permission message
    
#     if request.method == 'POST':
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             attendance = form.save(commit=False)
#             attendance.teacher = Teacher.objects.get(user=request.user)
#             attendance.save()
#             return redirect('success')  # Redirect to a success page
#     else:
#         form = AttendanceForm()

#     return render(request, 'mark_attendance.html', {'form': form})



# @login_required
# def no_permission(request):
#     return render(request, 'no_permission.html')

# # @login_required
# def view_grades(request):
#     if not request.user.groups.filter(name='Student').exists():
#         return redirect('no_permission')

#     student_profile = Student.objects.get(user=request.user)
#     grades = student_profile.grades.all()  # Assuming Student has related grades

#     return render(request, 'view_grades.html', {'grades': grades})


# def principal(request):
#     # Fetch query parameters for filtering
#     department_id = request.GET.get('department', '')
#     semester_id = request.GET.get('semester', '')
#     honors_minors_id = request.GET.get('honors_minors', '')
#     status = request.GET.get('status', '')
#     search_query = request.GET.get('search', '')

#     # Start with all students
#     students = Student.objects.all()

#     if department_id:
#         students = students.filter(department_id=department_id)
#     if semester_id:
#         even_sem = EvenSem.objects.filter(id=semester_id).first()
#         odd_sem = OddSem.objects.filter(id=semester_id).first()
#         students = students.filter(even_sem=even_sem) | students.filter(odd_sem=odd_sem)
#     if honors_minors_id:
#         students = students.filter(honors_minors_id=honors_minors_id)
#     if status:
#         students = students.filter(status=status)
#     if search_query:
#         students = students.filter(name__icontains=search_query)

#     # Fetch other data for the dropdowns
#     departments = Department.objects.all()
#     even_sems = EvenSem.objects.all()
#     odd_sems = OddSem.objects.all()
#     honors_minors = HonorsMinors.objects.all()
#     statuses = Student.objects.values_list('status', flat=True).distinct()

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         # Return HTML snippet for the table rows only
#         context = {
#             'students': students,
#         }
#         return render(request, 'student_table_rows.html', context)

#     context = {
#         'students': students,
#         'departments': departments,
#         'all_semesters': list(even_sems) + list(odd_sems),
#         'honors_minors': honors_minors,
#         'statuses': statuses,
#     }

#     return render(request, 'principal.html', context)






# def index(request):
#     return render(request, 'index.html')



# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user_profile, created = Profile.objects.get_or_create(user=user)
#             user_profile.user_type = form.cleaned_data['user_type']
#             user_profile.save()

#             user_type = form.cleaned_data['user_type']
#             if user_type == 'TEACHER':
#                 group, created = Group.objects.get_or_create(name='Teacher')
#                 user.groups.add(group)
#                 user.is_staff = True
#                 user.save()
#                 faculty_id = form.cleaned_data.get('faculty_id')  # Get the faculty_id
#                 create_or_update_teacher(user, faculty_id)

#             elif user_type == 'PRINCIPAL':
#                 group, created = Group.objects.get_or_create(name='Principal')
#                 user.groups.add(group)
#                 user.is_staff = True
#                 user.is_superuser = True
#                 user.save()

#             auth_login(request, user)  # Automatically log in the user
#             return redirect('login')  # Or another page you prefer
#     else:
#         form = UserRegistrationForm()

#     return render(request, 'register.html', {'form': form})




# from django.shortcuts import render
# from django.contrib.auth.models import Group, Permission

# def manage_permissions(request):
#     if request.user.is_superuser:
#         if request.method == 'POST':
#             # Implement logic to add or remove permissions based on user input
#             pass
#         groups = Group.objects.all()
#         permissions = Permission.objects.all()
#         return render(request, 'manage_permissions.html', {'groups': groups, 'permissions': permissions})
#     else:
#         return render(request, 'permission_denied.html')

# def permission_denied(request):
#     return render(request, 'permission_denied.html')

# from django.shortcuts import render, redirect
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

# def update_permissions(request):
#     if request.method == 'POST':
#         # Handle standard permissions
#         permission_groups = {
#             'Principal': request.POST.getlist('principal_perms'),
#             'HOD': request.POST.getlist('hod_perms'),
#             'Teacher': request.POST.getlist('teacher_perms'),
#             'Staff': request.POST.getlist('staff_perms'),
#             'Student': request.POST.getlist('student_perms'),
#         }

#         for group_name, perms in permission_groups.items():
#             group = Group.objects.get(name=group_name)
#             # Remove all existing permissions
#             group.permissions.clear()
#             # Add selected permissions
#             for perm_codename in perms:
#                 try:
#                     permission = Permission.objects.get(codename=perm_codename)
#                     group.permissions.add(permission)
#                 except Permission.DoesNotExist:
#                     continue

#         # Handle special permissions
#         if 'is_staff' in request.POST:
#             request.user.is_staff = True
#         else:
#             request.user.is_staff = False
        
#         if 'is_superuser' in request.POST:
#             request.user.is_superuser = True
#         else:
#             request.user.is_superuser = False

#         request.user.save()

#         return redirect('manage_permissions')  # Redirect to the page displaying updated permissions

#     # Render the form with current permissions
#     return render(request, 'manage_permissions.html', {
#         'principal_perms': get_permissions_for_group('Principal'),
#         'hod_perms': get_permissions_for_group('HOD'),
#         'teacher_perms': get_permissions_for_group('Teacher'),
#         'staff_perms': get_permissions_for_group('Staff'),
#         'student_perms': get_permissions_for_group('Student'),
#         'user': request.user
#     })

# def get_permissions_for_group(group_name):
#     group = Group.objects.get(name=group_name)
#     content_types = ContentType.objects.all()
#     permissions = Permission.objects.filter(content_type__in=content_types)
#     perm_list = []
#     for perm in permissions:
#         perm_list.append({
#             'codename': perm.codename,
#             'name': perm.name,
#             'is_checked': perm in group.permissions.all()
#         })
#     return perm_list
