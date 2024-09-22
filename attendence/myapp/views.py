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

def student_form(request):
    # Dummy student data
    students = [
        {'id': 1, 'name': 'John Doe', 'roll_number': '101'},
        {'id': 2, 'name': 'Jane Smith', 'roll_number': '102'},
        {'id': 3, 'name': 'Alice Johnson', 'roll_number': '103'},
        {'id': 4, 'name': 'Bob Brown', 'roll_number': '104'},
        {'id': 5, 'name': 'Charlie Davis', 'roll_number': '105'},
        {'id': 6, 'name': 'David White', 'roll_number': '106'},
        {'id': 7, 'name': 'Emma Watson', 'roll_number': '107'},
        {'id': 8, 'name': 'Franklin Pierce', 'roll_number': '108'},
        {'id': 9, 'name': 'Grace Hopper', 'roll_number': '109'},
        {'id': 10, 'name': 'Hannah Lee', 'roll_number': '110'},
        {'id': 11, 'name': 'Ian McKellen', 'roll_number': '111'},
        {'id': 12, 'name': 'Jackie Chan', 'roll_number': '112'},
        {'id': 13, 'name': 'Katherine Zeta', 'roll_number': '113'},
        {'id': 14, 'name': 'Liam Hemsworth', 'roll_number': '114'},
        {'id': 15, 'name': 'Monica Geller', 'roll_number': '115'},
        {'id': 16, 'name': 'Nina Dobrev', 'roll_number': '116'},
        {'id': 17, 'name': 'Olivia Pope', 'roll_number': '117'},
        {'id': 18, 'name': 'Paul Newman', 'roll_number': '118'},
        {'id': 19, 'name': 'Quincy Adams', 'roll_number': '119'},
        {'id': 20, 'name': 'Rachel Green', 'roll_number': '120'},
        {'id': 21, 'name': 'Sam Wilson', 'roll_number': '121'},
        {'id': 22, 'name': 'Tina Fey', 'roll_number': '122'},
        {'id': 23, 'name': 'Uma Thurman', 'roll_number': '123'},
        {'id': 24, 'name': 'Victor Hugo', 'roll_number': '124'},
        {'id': 25, 'name': 'Wanda Maximoff', 'roll_number': '125'},
        {'id': 26, 'name': 'Xavier Woods', 'roll_number': '126'},
        {'id': 27, 'name': 'Yasmin Bleeth', 'roll_number': '127'},
        {'id': 28, 'name': 'Zachary Quinto', 'roll_number': '128'},
    ]

    if request.method == 'POST':
        # Process attendance for each student
        for student in students:
            attendance_status = request.POST.get(f'attendance_{student["id"]}', 'absent')
            # Here you can replace the logic to save the attendance in the database.
            # For example:
            # Attendance.objects.create(student_id=student["id"], status=attendance_status)
            print(f"Student {student['name']} ({student['roll_number']}): {attendance_status}")

        return redirect('student_form')  # Redirect to the form after submission

    # Render the student form with the list of students
    return render(request, 'student_form.html', {'students': students})

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
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')

    hod_profile = get_object_or_404(HOD, user=request.user)
    department = hod_profile.department

    teachers = Teacher.objects.filter(department=department)
    students = Student.objects.filter(department=department)

    return render(request, 'hod_dashboard.html', {'department': department, 'teachers': teachers, 'students': students})

@login_required
def manage_teachers(request):
    if not (request.user.groups.filter(name='HOD').exists() or request.user.groups.filter(name='Principal').exists()):
        return redirect('no_permission')

    hod_profile = get_object_or_404(HOD, user=request.user)
    department = hod_profile.department
    teachers = Teacher.objects.filter(department=department)

    return render(request, 'manage_teachers.html', {'teachers': teachers})

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

# Edit Student View
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('view_student_details')
    else:
        form = StudentForm(instance=student)
    return render(request, 'add_edit_student.html', {'form': form, 'action': 'Edit'})

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
