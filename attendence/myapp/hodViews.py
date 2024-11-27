
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Q
from django.views import View

from .models import (
    Labs,
    Batches,
    Teacher,
    Student,
    Course,
    Attendance,
    Semester,
    Year,
    Department,
    LabsBatches,
)





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

    return render(request, 'dashboardtemplates/HOD_Dashboard.html', {'attendance_data': attendance_data, 'years': years})




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
