from django.shortcuts import render, redirect
from .models import Teacher
from django.shortcuts import get_object_or_404
from .models import Year, Student

def HOD_Dashboard(request):
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')
    
    if request.user.groups.filter(name='Principal').exists():
        is_hod = False
        is_principal = True
    elif request.user.groups.filter(name='HOD').exists():
        is_hod = True
        is_principal = False
    else:
        is_hod = False
        is_principal = False
        
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

    return render(request, 'hodtemplates/hod_dashboard.html', {'attendance_data': attendance_data, 'years': years, 'teacher': teacher, 'is_hod': is_hod, 'is_principal': is_principal})
