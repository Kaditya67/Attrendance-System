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

from .forms import TeacherUpdateForm
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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentUpdateForm

@login_required
def update_student_profile(request):
    # Get the current student's profile
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('StudentDashBoard', student_id=student.student_id)
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, 'student/update_profile.html', {'form': form})

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
def SubjectDetails(request, student_id, course_id):
    # Fetch the student using the student_id
    student = get_object_or_404(Student, student_id=student_id)
    
    # Fetch the course using the course_id
    course = get_object_or_404(Course, id=course_id)
    
    # Retrieve the attendance records for this student and course
    attendance_records = Attendance.objects.filter(student=student, course=course).order_by('date')
    
    # Pass the attendance records to the template
    return render(request, 'SubjectDetails.html', {
        'student': student,
        'course': course,
        'attendance_records': attendance_records,
    })



# View for subject attendance details
@login_required
def Subject_Attendance_Details(request):
    return render(request, 'teachertemplates/Subject_Attedance_Details.html')

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

    return render(request, 'StudentDashBoard.html', {
        'student': student,
        'attendance_summary': attendance_data,
        'average_attendance': average_attendance,  # Pass the average attendance to the template
        'missed_attendance': missed_attendance,    # Pass the missed attendance to the template
    })


# View for principal dashboard
def PrincipalDashboard(request):
    # Logic for displaying principal dashboard
    return render(request, 'PrincipalDashboard.html')

# View for HOD dashboard
# views.py

from django.shortcuts import render
from .models import Year, Student, Attendance

from django.shortcuts import render
from django.http import JsonResponse
from .models import Year, Student, Attendance

def HOD_Dashboard(request):
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')
    
    teacher =  get_object_or_404(Teacher, user=request.user)
    
    # Fetch all years
    years = Year.objects.all()
    attendance_data = []

    for year in years:
        # Fetch all students in this year
        students = Student.objects.filter(semester__year=year.name)
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

    return render(request, 'HOD_Dashboard.html', {'attendance_data': attendance_data, 'years': years, 'teacher': teacher})


from django.http import JsonResponse
from .models import Semester, Course  # Import the necessary models

def get_subjects_by_year(request):
    year_code = request.GET.get('year_code')
    
    # Fetch all semesters that belong to the selected year
    semester_objects = Semester.objects.filter(year=year_code)
    
    subjects = []
    
    # Fetch all courses related to each semester
    for semester in semester_objects:
        for course in semester.courses.all():  # Fetch all courses related to the semester
            # Get total classes and classes attended by students
            total_classes = Attendance.objects.filter(course=course).count()  # Total classes for this course
            classes_attended = Attendance.objects.filter(course=course, present=True).count()  # Classes attended by students
            
            # Get total students for the course (You might want to adjust this based on your enrollment logic)
            total_students = Student.objects.filter(semester=semester).count()  # Count of students in the current semester
            
            # Calculate class attended using the provided formula
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
from .models import Course, Attendance

from django.http import JsonResponse
from .models import Course, Attendance, Student

from django.http import JsonResponse
from .models import Course, Attendance, Student

def get_students_by_subject(request):
    subject_code = request.GET.get('subject_code')

    try:
        course = Course.objects.get(code=subject_code)
    except Course.DoesNotExist:
        return JsonResponse({'students': [], 'error': 'Course not found'}, status=404)

    # Fetch attendance records for the selected course
    attendances = Attendance.objects.filter(course=course)

    # Prepare student data and a set to track unique student IDs
    student_data = []
    seen_students = set()  # To track unique students

    for attendance in attendances:
        student = attendance.student
        
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
        
        # Fetch all students in this year
        students = Student.objects.filter(semester__year=year_code)
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

        return render(request, 'attendance_details.html', context)


from django.http import JsonResponse
from django.shortcuts import render
from .models import Year, Semester, Course

def subject_attendance(request):
    years = Year.objects.all()
    return render(request, 'subject_attendance.html', {'years': years})

# def get_subjects_by_year(request):
#     year_code = request.GET.get('year_code')
#     semester_objects = Semester.objects.filter(year=year_code)
    
#     # Fetch all courses for the retrieved semesters
#     subjects = []
#     for semester in semester_objects:
#         subjects.extend(semester.courses.all())  # Fetch all courses related to each semester

#     # Create a list of course names to return as JSON
#     subject_names = [{'code': course.code, 'name': course.name} for course in subjects]
#     return JsonResponse({'subjects': subject_names})


from django.shortcuts import render, redirect
from .models import Semester, Course

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
                return redirect('HOD_Dashboard')
            elif user.groups.filter(name='Teacher').exists():
                return redirect('teacher_dashboard')
            elif user.groups.filter(name='Student').exists():
                try:
                    student = Student.objects.get(user=user)
                    return redirect('StudentDashBoard', student_id=student.student_id)
                except Student.DoesNotExist:
                    return redirect('dashboard')
                # return redirect('student_dashboard')
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

