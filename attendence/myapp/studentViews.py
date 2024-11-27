from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance
from django.db.models import Count, Q
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
