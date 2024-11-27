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

    return render(request, 'studenttemplates/StudentDashBoard.html', {
        'student': student,
        'attendance_summary': attendance_data,
        'average_attendance': average_attendance,  # Pass the average attendance to the template
        'missed_attendance': missed_attendance,    # Pass the missed attendance to the template
    })


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student
from .forms import StudentUpdateForm  # Assuming you have a form for Student similar to TeacherUpdateForm


def update_student(request, student_id):
    if request.user.groups.filter(name='HOD').exists():
        is_hod = True
        is_principal = False
    elif request.user.groups.filter(name='Principal').exists():
        is_hod = False
        is_principal = True
    else:
        is_hod = False
        is_principal = False

    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = StudentUpdateForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('update_student', student_id=student.id)  # Redirect to the same page to show message

        elif 'change_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if new_password1 == new_password2 and student.user.check_password(old_password):
                student.user.set_password(new_password1)
                student.user.save()
                update_session_auth_hash(request, student.user)  # Important to keep the user logged in
                messages.success(request, 'Password changed successfully!')
                return redirect('update_student', student_id=student.id)  # Redirect to the same page to show message
            else:
                messages.error(request, 'Password change failed. Please check your inputs.')

    else:
        form = StudentUpdateForm(instance=student)

    context = {
        'form': form,
        'student': student,
        'is_hod': is_hod,
        'is_principal': is_principal
    }
    return render(request, 'studenttemplates/update_student.html', context)
