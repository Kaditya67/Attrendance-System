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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher, Attendance, Course
from django.db.models import Max



# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Labs, Batches

def add_batches(request, lab_id):
    lab = get_object_or_404(Labs, id=lab_id)
    batch_instance, created = Batches.objects.get_or_create(lab=lab)
    
    if request.method == 'POST':
        batch_input = request.POST.get('batch_options')  # Example: "a,b,c"
        batch_list = [batch.strip() for batch in batch_input.split(',')]  # Split by commas
        batch_instance.set_batch_options(batch_list)
        return redirect('assign_batches', lab_id=lab.id)

    context = {
        'lab': lab,
        'batch_options': batch_instance.get_batch_options(),  # Retrieve the current batch options
    }
    return render(request, 'add_batches.html', context)


# View to delete batches from a lab
from django.shortcuts import get_object_or_404, redirect
from .models import Batches  # Make sure to import your Batches model

def delete_batch(request, batch_id):
    if batch_id == 0:
        # Handle the logic for deleting the created batch
        # You may want to find the appropriate batch to delete based on some criteria
        # For example, if you have only one "default" batch to delete, fetch it
        batch = Batches.objects.first()  # Or implement your own logic to find the right batch
    else:
        # Otherwise, retrieve the batch as normal
        batch = get_object_or_404(Batches, id=batch_id)
    
    lab_id = batch.lab.id  # Get the associated lab ID
    batch.delete()  # Delete the batch
    return redirect('lab_detail', lab_id=lab_id)  # Redirect to lab detail page



# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Labs, Batches, Student
import json

# def assign_batches_to_students(request, lab_id):
#     lab = get_object_or_404(Labs, id=lab_id)
#     batch_obj = lab.batches.first()  # Get the first batch object associated with the lab

#     # Parse the batch options into a list
#     if batch_obj:
#         batch_options = json.loads(batch_obj.batch_options)  # Parse JSON string to list
#     else:
#         batch_options = []

#     students = Student.objects.filter(semester=lab.semester)  # Filter students based on lab semester

#     if request.method == 'POST':
#         for student in students:
#             selected_batch = request.POST.get(f'batch_{student.id}')  # Get batch for each student
#             student.assign_batch(lab.index, selected_batch)  # Assign batch based on lab index

#         return redirect('labs')  # Redirect after successful assignment

#     return render(request, 'assign_batches.html', {'lab': lab, 'batch_options': batch_options, 'students': students})


def assign_batches_to_students(request, lab_id):
    lab = get_object_or_404(Labs, id=lab_id)
    batch_obj = lab.batches.first()

    if batch_obj:
        batch_options = json.loads(batch_obj.batch_options)
    else:
        batch_options = []

    students = Student.objects.filter(semester=lab.semester)

    if request.method == 'POST':
        for student in students:
            selected_batch = request.POST.get(f'batch_{student.id}')
            if selected_batch:
                student.assign_batch(lab.index, selected_batch)

        # Redirect to the lab dashboard after assignment
        return redirect('lab_detail', lab_id=lab.id)

    return render(request, 'assign_batches.html', {'lab': lab, 'batch_options': batch_options, 'students': students})


import json

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



from django.shortcuts import render
from .models import Labs, Batches

@login_required
def lab_dashboard(request):
        # Get the logged-in teacher
    teacher = get_object_or_404(Teacher, user=request.user)
    labs = teacher.assigned_labs.all()
    print(f"Assigned Labs: {labs}")

    lab_data = []

    for lab in labs:
        lab_data.append({
            'lab_id': lab.id,
            'lab_name': lab.name,
            'lab_semester': lab.semester,
            'lab_index': lab.index,
        })
    print(f"Lab Data: {lab_data}")

    context = {
        'lab': lab_data,
        'labs': labs,  # Include all labs for navbar display
    }
    return render(request, 'lab_dashboard.html', context)


# views.py

from django.shortcuts import render, get_object_or_404
from .models import Labs, Batches

import json

def lab_detail(request, lab_id):
    lab = get_object_or_404(Labs, id=lab_id)
    batches = lab.batches.all()  # Get all batches for the lab
    students = Student.objects.filter(semester=lab.semester) 
    print(students)

    index = lab.index

    for batch in batches:
        batch.batch_options = json.loads(batch.batch_options)  # Ensure it's a list

    batch_student_data = []
    # Iterate over each batch
    for batch in batches[0].batch_options:
        match_students = []
        for student in students:
            if(student.batches[str(index)] == batch):
                print(f'Batch: {batch}, Student: {student}')
                match_students.append({
                    'batch': batch,
                    'student': student
                })

        batch_student_data.append({
            'batch': batch,
            'match_students':match_students
        })
    
    print(f"Students and Batches {batch_student_data}")
        

    context = {
        'lab': lab,
        'batches': batches,  # Pass all batches
        'batch_student_data': batch_student_data
    }
    return render(request, 'lab_detail.html', context)

from django.shortcuts import render
from .models import Attendance  # Adjust the import based on your project structure

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher, Course, Attendance
from collections import defaultdict

from collections import defaultdict
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Teacher, Course, Attendance

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import Teacher, Course, Attendance

@login_required
def view_attendance(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = teacher.assigned_courses.all()

    selected_course = None
    attendance_summary = []

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        selected_course = get_object_or_404(Course, id=subject_id)

        # Fetch all attendance records for the selected course
        attendance_records = Attendance.objects.filter(course=selected_course)

        if not attendance_records.exists():
            messages.warning(request, "No attendance records found for the selected course.")
            return redirect('view_attendance')

        # Summarize attendance records by date and count
        summary = defaultdict(lambda: [0, '', 0])  # [total present, common notes, count]
        for record in attendance_records:
            # Only aggregate if the current count is greater than the previously saved count for that date
            summary[(record.date, record.count)][0] += record.present  # Total present
            summary[(record.date, record.count)][1] = record.notes  # Get notes
            summary[(record.date, record.count)][2] = record.count  # Use the last count found

        # Convert the summary to a list for rendering
        attendance_summary = [
            (date, total_present, notes, count) 
            for (date, count), (total_present, notes, _) in summary.items()
        ]

    context = {
        'courses': courses,
        'attendance_summary': attendance_summary,
        'selected_course': selected_course,
    }
    return render(request, 'teachertemplates/view_attendance.html', context)


# @login_required
# def view_attendance(request):
#     teacher = get_object_or_404(Teacher, user=request.user)
#     courses = teacher.assigned_courses.all()

#     selected_course = None
#     attendance_summary = []

#     if request.method == 'POST':
#         subject_id = request.POST.get('subject')
#         selected_course = get_object_or_404(Course, id=subject_id)

#         # Fetch all attendance records for the selected course
#         attendance_records = Attendance.objects.filter(course=selected_course)

#         if not attendance_records.exists():
#             messages.warning(request, "No attendance records found for the selected course.")
#             return redirect('view_attendance')

#         # Summarize attendance records by date
#         summary = defaultdict(lambda: [0, ''])  # [total present, common notes]
#         for record in attendance_records:
#             summary[record.date][0] += 1 if record.present else 0
#             summary[record.date][1] = record.notes  # You can modify how to aggregate notes

#         # Convert the summary to a list for rendering
#         attendance_summary = [(date, total_present, notes) for date, (total_present, notes) in summary.items()]

#     context = {
#         'courses': courses,
#         'attendance_summary': attendance_summary,
#         'selected_course': selected_course,
#     }
#     return render(request, 'teachertemplates/view_attendance.html', context)

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

from django.urls import reverse  
@login_required
def select_course_lecture(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = teacher.assigned_courses.all()

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')

        course = get_object_or_404(Course, id=subject_id)
        attendance_records = Attendance.objects.filter(course=course, date=date)

        if not attendance_records.exists():
            messages.warning(request, "No attendance records found for the selected date.")
            return redirect('select_course_lecture')

        max_count = attendance_records.aggregate(Max('count'))['count__max']
        lecture_numbers = list(range(1, max_count + 1))

        context = {
            'courses': courses,
            'lecture_numbers': lecture_numbers,
            'selected_course': course,
            'selected_date': date,
        }

        # Redirect to edit attendance page after selecting the course and lecture
        lecture_number = request.POST.get('lecture_number')
        if lecture_number:
            return redirect(reverse('edit_attendance', args=[subject_id, date, lecture_number]))
        
        return render(request, 'teachertemplates/select_lecture.html', context)

    context = {'courses': courses}
    return render(request, 'teachertemplates/select_lecture.html', context)


@login_required
def edit_attendance(request, subject_id, date, lecture_number):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = teacher.assigned_courses.all()

    # Fetch the selected course
    course = get_object_or_404(Course, id=subject_id)

    # Fetch attendance records for the selected course, date, and lecture number
    attendance_records = Attendance.objects.filter(course=course, date=date, count=lecture_number)

    if not attendance_records.exists():
        messages.warning(request, "No attendance records found for the selected lecture.")
        return redirect('select_course_lecture')  # Redirect to course selection page if no records found

    if request.method == 'POST':
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
            return redirect('select_course_lecture')  # Redirect to selection page after update
        else:
            messages.warning(request, "No attendance records were updated.")

    context = {
        'courses': courses,
        'attendance_records': attendance_records,
        'selected_course': course,
        'selected_date': date,
        'lecture_number': lecture_number,
    }

    return render(request, 'teachertemplates/edit_attendance.html', context)


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

@login_required
def submit_attendance(request):
    if request.method == "POST":
        print("Received POST request for submit_attendance")
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        common_notes = request.POST.get('common_notes', '')
        absent_students = request.POST.get('absent_students', '').split(',')
        
        print(f"Subject ID: {subject_id}, Date: {date}, Common Notes: {common_notes}, Absent Students: {absent_students}")
        course = Course.objects.get(id=subject_id)
        print(f"Course: {course}")
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

# View for class report
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Labs, Teacher  # Adjust based on your app's structure
from django.contrib.auth.decorators import login_required

@login_required
def Class_Report(request):
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

