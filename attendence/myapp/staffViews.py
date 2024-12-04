from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from collections import defaultdict
import json
from django.urls import reverse  
from .models import Labs, Batches, Staff, Teacher, Student, Course, Attendance, Semester, LabsBatches
import openpyxl
from .forms import LabForm, TeacherUpdateForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER
from tkinter import CENTER


def error(request):
    return render(request,'error.html')


from django.shortcuts import render
from .models import Department, Semester, Student, Staff

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Staff, Semester, Course, Student

# semesters
# @login_required
# def staff_dashboard(request):
#     # Get the staff member associated with the logged-in user
#     staff = get_object_or_404(Staff, user=request.user)
#     department = staff.assigned_department  # Get the assigned department

#     # Get all semesters for the assigned department
#     semesters = Semester.objects.filter(session_year__department=department)

#     # Collect courses and corresponding students
#     course_data = []
#     for semester in semesters:
#         courses = Course.objects.filter(semester=semester)
#         for course in courses:
#             students_in_course = Student.objects.filter(semester=semester).distinct()

#             course_data.append({
#                 'course': course,
#                 'semester': semester,
#                 'students': students_in_course,
#             })
#             print(course_data)

#     context = {
#         'course_data': course_data,
#         'staff': staff,
#         'department': department,
#         'semesters': semesters,
#         'user':request.user,
#     }

#     return render(request, 'stafftemplates/add_staff_attendance         .html', context)




from django.http import JsonResponse

def get_courses(request):
    semester_id = request.GET.get('semester_id')  # Get the selected semester ID
    if semester_id:
        # Fetch courses for the selected semester
        courses = Course.objects.filter(semester_id=semester_id).values('id', 'name')
        return JsonResponse({'courses': list(courses)})
    return JsonResponse({'error': 'Invalid semester ID'}, status=400)






from django.http import JsonResponse
from .models import Course, Student

from django.http import JsonResponse

def get_students_for_course(request):
    course_id = request.GET.get('course_id')  # Get the selected course ID

    if course_id:
        try:
            # Fetch the selected course
            course = Course.objects.get(id=course_id)

            # Fetch the students enrolled in the semester of the selected course
            students = Student.objects.filter(semester=course.semester)

            # Extract student details (name and roll number)
            student_details = [
                {
                    'name': student.user.username,
                    'roll_number': student.roll_number
                }
                for student in students
            ]

            return JsonResponse({'students': student_details})
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found.'}, status=404)

    return JsonResponse({'error': 'Invalid course ID.'}, status=400)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import json
from django.http import JsonResponse

@csrf_exempt
def save_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received Data:", data)  # Debug incoming data
            
            course_id = data.get('course_id')
            date = data.get('date')
            attendance_records = data.get('attendance_records', [])

            if not course_id or not date or not attendance_records:
                return JsonResponse({'success': False, 'error': 'Missing required fields'})

            # Save attendance for each student
            for record in attendance_records:
                student_id = record.get('student_id')
                present = record.get('present', False)
                print(f"Saving attendance for Student {student_id}: Present={present}")  # Debug each record
                
                # Save to your Attendance model
                Attendance.objects.create(
                    course_id=course_id,
                    student_id=student_id,  # student_id is now correctly treated as a string
                    present=present,  # Use the correct field name
                    date=date
                )

            return JsonResponse({'success': True})
        except Exception as e:
            print("Error:", e)  # Debug the exception
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def Add_staff_Attendance(request):
    staff = get_object_or_404(Staff, user=request.user)
    department = staff.assigned_department  # Get the assigned department

    # Get all semesters for the assigned department
    semesters = Semester.objects.filter(session_year__department=department)
    if request.method == "POST":
        semester_id = request.POST.get('semester')  # Get selected semester ID
        semester = get_object_or_404(Semester, id=semester_id)
        print("Semester : ",semester)

        # Get all courses for the selected semester
        courses = semester.courses.all()

        course_data = []
        for course in courses:
            students_in_semester = Student.objects.filter(semester=semester).distinct()

            course_data.append({
                'course': course,
                'semester': semester,
                'students': students_in_semester,
            })
        
        context = {
            'course_data': course_data, 
            'staff': staff,
            'semester': semester,  # Pass the selected semester to the template
        }
        return render(request, 'stafftemplates/add_staff_attendance.html', context)

    context = {
        'staff': staff,
        'department': department,
        'semesters': semesters, 
    }
    return render(request, 'stafftemplates/add_staff_attendance.html', context)

def get_staff_courses(request,semester):
    courses = semester.courses.all()

    course_data = []
    for course in courses: 
        students_in_semester = Student.objects.filter(semester=semester).distinct()  # Fetch distinct students for the semester

        # Append course, semester, and students information to course_data
        course_data.append({
            'course': course,
            'semester': semester,
            'students': students_in_semester,
        })

    return course_data


@login_required
def fetch_staff_students(request):
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
            'course_data': get_staff_courses(request,semester),  # Function to fetch teacher's courses
        }

        return render(request, 'stafftemplates/add_staff_attendance.html', context)
    
    return redirect('Add_staff_Attendance')


@login_required
def submit_staff_attendance(request):
    if request.method == "POST":
        # print("Received POST request for submit_attendance")
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        common_notes = request.POST.get('common_notes', '')
        absent_students = request.POST.get('absent_students', '').split(',')
        
        # print(f"Subject ID: {subject_id}, Date: {date}, Common Notes: {common_notes}, Absent Students: {absent_students}")
        course = Course.objects.get(id=subject_id)
        # print(f"Course: {course}")
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

        return redirect('Add_staff_Attendance')

    return redirect('Add_staff_Attendance')






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Max
from .models import Staff, Semester, Course, Attendance, Student

@login_required
def Update_staff_Attendance(request):
    staff = get_object_or_404(Staff, user=request.user)
    department = staff.assigned_department  # Get the assigned department

    # Get all semesters for the assigned department
    semesters = Semester.objects.filter(session_year__department=department)

    if request.method == "POST":

        if 'update_attendance' in request.POST and 'lecture_number' in request.POST:
            print("Update attendance request received.")  # Debugging line
            subject_id = request.POST.get('subject')
            date = request.POST.get('date')
            lecture_number = request.POST.get('lecture_number')

            print(f"Subject ID: {subject_id}, Date: {date}, Lecture Number: {lecture_number}")  # Debugging line

            course = get_object_or_404(Course, id=subject_id)
            print(f"Course: {course.name}")  # Debugging line

            attendance_records = Attendance.objects.filter(course=course, date=date, count=lecture_number)
            print(f"Attendance records count: {attendance_records.count()}")  # Debugging line

            attendance_updated = 0
            for record in attendance_records:
                student_id = record.student.id
                attendance_status = request.POST.get(f'attendance_{student_id}', None)
                print(f"Processing Student ID: {student_id}, Current Status: {record.present}, Submitted Status: {attendance_status}")  # Debugging line

                if attendance_status is not None:
                    new_status = (attendance_status == 'Present')
                    if record.present != new_status:
                        record.present = new_status
                        record.save()
                        attendance_updated += 1
                        print(f"Updated: Student {student_id} to {'Present' if new_status else 'Absent'}")  # Debugging line
                    else:
                        print(f"No change for Student ID: {student_id}.")  # Debugging line
                else:
                    print(f"No attendance status provided for Student ID: {student_id}.")  # Debugging line

            if attendance_updated > 0:
                messages.success(request, f"{attendance_updated} attendance records updated successfully!")
                print(f"{attendance_updated} attendance records updated successfully!")  # Debugging line
            else:
                messages.warning(request, "No attendance records were updated.")
                print("No attendance records were updated.")  # Debugging line

            # Re-render the page with updated attendance records
            context = {
                'semesters': semesters,
                'attendance_records': attendance_records,
                'selected_course': course,
                'selected_date': date,
                'lecture_number': lecture_number,
                'staff': staff,
                'department': department,
            }
            return render(request, 'stafftemplates/Update_staff_Attendance.html', context)
    
        # Step 1: Fetch attendance records (Subject and Date selection)
        elif 'fetch' in request.POST:
            subject_id = request.POST.get('subject')  # Get selected course ID
            date = request.POST.get('date')  # Get selected date
            
            # Validate the course and fetch attendance records
            course = get_object_or_404(Course, id=subject_id)
            attendance_records = Attendance.objects.filter(course=course, date=date)

            if not attendance_records.exists():
                messages.warning(request, "No attendance records found for the selected date.")
                return redirect('Update_staff_Attendance')

            # Calculate lecture numbers based on attendance records
            max_count = attendance_records.aggregate(Max('count'))['count__max']
            lecture_numbers = list(range(1, max_count + 1))

            # Prepare context for rendering the template
            context = {
                'semesters': semesters,  # Keep semesters for dropdown
                'lecture_numbers': lecture_numbers,  # Add lecture numbers
                'selected_course': course,
                'selected_date': date,
                'staff': staff,
                'department': department,
            }
            return render(request, 'stafftemplates/Update_staff_Attendance.html', context)

        # Step 2: Load attendance for a specific lecture number
        elif 'lecture_number' in request.POST:
            subject_id = request.POST.get('subject')
            date = request.POST.get('date')
            lecture_number = request.POST.get('lecture_number')

            course = get_object_or_404(Course, id=subject_id)
            attendance_records = Attendance.objects.filter(course=course, date=date, count=lecture_number)

            context = {
                'semesters': semesters,
                'attendance_records': attendance_records,
                'selected_course': course,
                'selected_date': date,
                'lecture_number': lecture_number,
                'staff': staff,
                'department': department,
            }
            return render(request, 'stafftemplates/Update_staff_Attendance.html', context)

        # Step 3: Update attendance records

        # Step 4: Semester selection (original functionality)
        semester_id = request.POST.get('semester')  # Get selected semester ID
        semester = get_object_or_404(Semester, id=semester_id)

        # Get all courses for the selected semester
        courses = semester.courses.all()

        course_data = []
        for course in courses:
            students_in_semester = Student.objects.filter(semester=semester).distinct()

            course_data.append({
                'course': course,
                'semester': semester,
                'students': students_in_semester,
            })
        
        context = {
            'course_data': course_data,
            'staff': staff,
            'semester': semester,  # Pass the selected semester to the template
        }
        return render(request, 'stafftemplates/Update_staff_Attendance.html', context)

    # Initial context for rendering the template
    context = {
        'staff': staff,
        'department': department,
        'semesters': semesters,
    }
    return render(request, 'stafftemplates/Update_staff_Attendance.html', context)



@login_required
def view_attendance(request):
    staff = get_object_or_404(Staff, user=request.user)
    department = staff.assigned_department  # Get the assigned department

    # Get all semesters for the assigned department
    semesters = Semester.objects.filter(session_year__department=department)

    selected_course = None
    attendance_summary = []
    course_data = []  # Initialize course_data

    if request.method == 'POST':
        semester_id = request.POST.get('semester')  # Get selected semester ID
        semester = get_object_or_404(Semester, id=semester_id)

        # Get all courses for the selected semester
        courses = semester.courses.all()

        for course in courses:
            students_in_semester = Student.objects.filter(semester=semester).distinct()

            course_data.append({
                'course': course,
                'semester': semester,
                'students': students_in_semester,
            })

        # If a course is selected, fetch attendance records for that course
        selected_course_id = request.POST.get('subject')  # Get selected course ID
        if selected_course_id:
            selected_course = get_object_or_404(Course, id=selected_course_id)
            attendance_records = Attendance.objects.filter(course=selected_course)

            if not attendance_records.exists():
                messages.warning(request, "No attendance records found for the selected course.")
                return redirect('view_attendance')

            # Summarize attendance records by date and count
            summary = defaultdict(lambda: [0, '', 0])  # [total present, common notes, count]
            for record in attendance_records:
                summary[(record.date, record.count)][0] += record.present  # Total present
                summary[(record.date, record.count)][1] = record.notes  # Get notes
                summary[(record.date, record.count)][2] = record.count  # Use the last count found

            # Convert the summary to a list for rendering
            attendance_summary = [
                (date, total_present, notes, count) 
                for (date, count), (total_present, notes, _) in summary.items()
            ]

    context = {
        'staff': staff,
        'semesters': semesters,
        'attendance_summary': attendance_summary,
        'selected_course': selected_course,
        'course_data': course_data,  # Include course data in context
    }
    return render(request, 'stafftemplates/view_attendance.html', context)



@login_required
def edit_staff_attendance(request, subject_id, date, lecture_number):
    staff = get_object_or_404(Staff, user=request.user)
    department = staff.assigned_department  # Get the assigned department

    # Get all semesters for the assigned department
    semesters = Semester.objects.filter(session_year__department=department)

    # Fetch the selected course
    course = get_object_or_404(Course, id=subject_id)

    # Fetch attendance records for the selected course, date, and lecture number
    attendance_records = Attendance.objects.filter(course=course, date=date, count=lecture_number)

    if not attendance_records.exists():
        messages.warning(request, "No attendance records found for the selected lecture.")
        return redirect('view_attendance')  # Redirect to the course selection page if no records found

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
            print("success")
            return redirect('view_attendance')  # Redirect back after successful update
            
        else:
            messages.warning(request, "No attendance records were updated.")
            print("fail")

    context = {
        'semesters': semesters,
        'attendance_records': attendance_records,
        'selected_course': course,
        'selected_date': date,
        'lecture_number': lecture_number,
        'staff': staff
    }

    return render(request, 'stafftemplates/edit_staff_attendance.html', context)
