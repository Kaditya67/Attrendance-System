from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from collections import defaultdict
import json
from django.urls import reverse  
from .models import Labs, Batches, Teacher, Student, Course, Attendance, Semester, LabsBatches
import openpyxl
from .forms import TeacherUpdateForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER
from tkinter import CENTER


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
    return render(request, 'teachertemplates/lab_dashboard.html', context)


def add_batches(request, lab_id):
    lab = get_object_or_404(Labs, id=lab_id)
    batch_instance, created = Batches.objects.get_or_create(lab=lab)
    
    if request.method == 'POST':
        batch_input = request.POST.get('batch_options')  # Example: "a,b,c"
        batch_list = [batch.strip() for batch in batch_input.split(',')]  # Split by commas
        batch_instance.set_batch_options(batch_list)
        return redirect('teachertemplates/assign_batches', lab_id=lab.id)

    context = {
        'lab': lab,
        'batch_options': batch_instance.get_batch_options(),  # Retrieve the current batch options
    }
    return render(request, 'teachertemplates/assign_batches', context)


def delete_batch(request, batch_id):
    if batch_id == 0:
        batch = Batches.objects.first()  # Or implement your own logic to find the right batch
    else:
        # Otherwise, retrieve the batch as normal
        batch = get_object_or_404(Batches, id=batch_id)
    
    lab_id = batch.lab.id  # Get the associated lab ID
    batch.delete()  # Delete the batch
    return redirect('lab_detail', lab_id=lab_id)  # Redirect to lab detail page


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

    return render(request, 'teachertemplates/assign_batches.html', {'lab': lab, 'batch_options': batch_options, 'students': students})


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
    return render(request, 'teachertemplates/lab_detail.html', context)


def update_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('Teacher_dashboard')  # Change this to your success URL
    else:
        form = TeacherUpdateForm(instance=teacher)

    context = {
        'form': form,
        'teacher': teacher
    }
    return render(request, 'teachertemplates/update_teacher.html', context)


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
        'teacher': teacher
    }
    return render(request, 'teachertemplates/view_attendance.html', context)


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
            'teacher': teacher
        }

        # Redirect to edit attendance page after selecting the course and lecture
        lecture_number = request.POST.get('lecture_number')
        if lecture_number:
            return redirect(reverse('edit_attendance', args=[subject_id, date, lecture_number]))
        
        return render(request, 'teachertemplates/select_lecture.html', context)

    context = {'courses': courses, 'teacher': teacher}
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
        'teacher': teacher
    }

    return render(request, 'teachertemplates/edit_attendance.html', context)


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
        'teacher': teacher
    }

    return render(request, 'teachertemplates/add_attendance.html', context)


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


def Subject_Attendance_Details(request):
    # Get the teacher object for the currently logged-in user
    teacher = get_object_or_404(Teacher, user=request.user)

    # Get all courses taught by the teacher
    courses = teacher.assigned_courses.all()

    course_data = []
    attendance_data = {}  # Initialize a dictionary to hold attendance data for each course

    for course in courses:
        semester = course.semester

        students_in_semester = Student.objects.filter(semester=semester).distinct()

        sample_student = students_in_semester.first()
        if sample_student:
            attendance_records = Attendance.objects.filter(course=course, student=sample_student).values('date', 'count').order_by('date')

            attendance_data[course.name] = []
            for record in attendance_records:
                attendance_data[course.name].append({
                    'date': record['date'],
                    'count': record['count']
                })

            student_data = []
            total_attended_sum = 0  # To sum total attended counts for average calculation
            student_count = 0  # To count the number of students

            for student in students_in_semester:
                total_attended = 0
                total_classes = len(attendance_data[course.name])
                attendance_records = []
                for date_record in attendance_data[course.name]:
                    date = date_record['date']
                    count = date_record['count']

                    attendance_instance = Attendance.objects.filter(course=course, student=student, date=date, count=count).first()
                    
                    is_present = attendance_instance.present if attendance_instance else None
                    attendance_records.append({
                        'date': date,
                        'latest_notes': attendance_instance.notes if attendance_instance else None,
                        'present': is_present,
                    })

                    if is_present:
                        total_attended += 1

                # Calculate percentage attendance for the student
                percentage = (total_attended / total_classes) * 100 if total_classes > 0 else 0

                # Add student attendance data including total_attended and percentage
                student_data.append({
                    'student': student,
                    'attendance': attendance_records,
                    'total_attended': total_attended,
                    'percentage': round(percentage, 2),  # Round the percentage to 2 decimal places
                })

                # Accumulate total attended counts and increment student count
                total_attended_sum += total_attended
                student_count += 1

            # Calculate the average attendance percentage for the course
            average_attendance = (total_attended_sum / (student_count * total_classes)) * 100 if student_count > 0 and total_classes > 0 else 0
            top_students = sorted(student_data, key=lambda x: x['percentage'], reverse=True)[:3]

            course_data.append({
                'course': course,
                'semester': semester,
                'students': student_data,
                'average_attendance': round(average_attendance, 2),  # Store the average attendance percentage
                'top_students': top_students,  # Add top students to course_data
            })

    return render(request, 'teachertemplates/Subject_Attedance_Details.html', {
        'teacher': teacher,
        'course_data': course_data,
        'attendance_data': attendance_data
    })


# Export to PDF
def export_students_to_pdf(semester_data,semester):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_attendance.pdf"'

    # Create the PDF object
    pdf = SimpleDocTemplate(response, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    # Define the styles for the document
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER

    # Add title
    elements.append(Paragraph("Student Attendance Report", title_style))

    # Add semester title
    if semester_data:
        semester_title = semester
        semester_heading = Paragraph(f"Semester: {semester_title}", styles['Heading2'])
        elements.append(semester_heading)

    # Define the table headers
    data = [["Student Name", "Course", "Total Classes", "Classes Attended", "Percentage"]]

    # Add student and course data to the table
    for semester in semester_data:
        for student in semester['student_data']:
            student_name = f"{student['student'].user.first_name} {student['student'].user.last_name}"

            for course in student['course_data']:
                data.append([
                    student_name,
                    course['course'].name,
                    course['total_count'],
                    course['count_present'],
                    f"{course['percentage']}%"
                ])

    # Create the table
    table = Table(data, colWidths=[2.5 * inch, 1.8 * inch, 1.2 * inch, 1.5 * inch, 1.2 * inch])

    # Add some style to the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all text
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font bold
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Body background
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # Body font size
    ]))

    # Add the table to the PDF elements
    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    return response



def export_students_to_excel(semester_data):
    # Create a response object for Excel file download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.xlsx"'

    # Create an Excel workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance Report"

    # Create headers
    headers = ["Student Name"]
    # Get course names dynamically from the first student in semester_data (assuming all students have the same courses)
    if semester_data and semester_data[0]['student_data']:
        for course_data in semester_data[0]['student_data'][0]['course_data']:
            headers.append(course_data['course'].name)
        headers.append("Overall Attendance")  # Add an overall attendance column

    # Append the headers to the worksheet
    ws.append(headers)

    # Iterate through semester_data to populate the rows
    for semester in semester_data:
        for student_data in semester['student_data']:
            student = student_data['student']  # Student object
            
            # Get student name from the user object
            student_name = f"{student.user.first_name} {student.user.last_name}"
            row = [student_name]

            # Iterate through courses and append attendance data
            for course_data in student_data['course_data']:
                attendance_info = f"{course_data['count_present']}/{course_data['total_count']} ({course_data['percentage']}%)"
                row.append(attendance_info)

            # Append overall attendance (same logic as shown in your table)
            if student_data['total_classes'] > 0:
                overall_attendance = f"{student_data['total_present']}/{student_data['total_classes']} ({student_data['total_present']/student_data['total_classes']*100:.2f}%)"
            else:
                overall_attendance = "0/0 (0%)"
            row.append(overall_attendance)

            # Append the row to the worksheet
            ws.append(row)

    # Save the workbook to the response
    wb.save(response)
    return response


# Class Report View with Export Functionality
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

# Class Report View with Export Functionality
def Class_Report(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    semesters = Semester.objects.filter(session_year=teacher.assigned_courses.first().semester.session_year)

    selected_semester = request.GET.get('semester')
    export_format = request.GET.get('format')  # Check if an export format (excel or pdf) is requested
    semester_data = []

    # If no semester is selected, return an error message or prompt
    if not selected_semester or selected_semester == 'None':
        # Show an error message on the page instead of throwing an error
        return render(request, 'teachertemplates/class_report.html', {
            'teacher': teacher,
            'semester_data': semester_data,
            'semesters': semesters,
            'selected_semester': None,
            'error_message': 'Please select a semester before exporting the report.'
        })

    # Try to convert selected_semester to integer (just in case)
    try:
        semester = get_object_or_404(Semester, id=int(selected_semester))
    except (ValueError, Semester.DoesNotExist):
        return HttpResponse("Invalid semester selected. Please select a valid semester.", status=400)

    # Now handle the case where a valid semester is selected
    students = Student.objects.filter(semester=semester)
    courses = Course.objects.filter(semester=semester)

    student_data_list = []
    for student in students:
        course_data_list = []
        total_present = 0
        total_classes = 0

        for course in courses:
            attendances = Attendance.objects.filter(student=student, course=course)
            total_count = attendances.count()
            count_present = attendances.filter(present=True).count()
            percentage = (count_present / total_count * 100) if total_count else 0

            course_data_list.append({
                'course': course,
                'total_count': total_count,
                'count_present': count_present,
                'percentage': round(percentage, 2),
            })

            total_present += count_present
            total_classes += total_count

        student_data_list.append({
            'student': student,
            'course_data': course_data_list,
            'total_present': total_present,
            'total_classes': total_classes,
        })

    semester_data.append({
        'semester': semester,
        'student_data': student_data_list,
    })

    # Handle export functionality
    if export_format == 'excel':
        return export_students_to_excel(semester_data)
    elif export_format == 'pdf':
        return export_students_to_pdf(semester_data,semester)

    return render(request, 'teachertemplates/class_report.html', {
        'teacher': teacher,
        'semester_data': semester_data,
        'semesters': semesters,
        'selected_semester': selected_semester
    })
