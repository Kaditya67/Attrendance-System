from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import (StudentRegistrationForm, TeacherRegistrationForm, 
                    HODRegistrationForm, StaffRegistrationForm, 
                    PrincipalRegistrationForm, UserLoginForm, AttendanceForm)
from .models import (Student, Teacher, HOD, Staff, Principal, Department, Semester,
                    #  EvenSem, OddSem, 
                     HonorsMinors)

def register_user(request, form_class, group_name, template_name, success_redirect):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            student = form.save()  # Save the form and get the Student instance
            user = student.user  # Access the associated User instance
            
            user_group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(user_group)  # Add the User to the group
            
            auth_login(request, user)  # Optional: Auto-login after registration
            
            messages.success(request, f"{group_name} registered successfully!")
            return redirect(success_redirect)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = form_class()

    return render(request, template_name, {'form': form})


def register_student(request):
    return register_user(request, StudentRegistrationForm, 'Student', 'register_student.html', 'student_dashboard')

def register_teacher(request):
    return register_user(request, TeacherRegistrationForm, 'Teacher', 'teacher_register.html', 'dash_teacher')

def register_hod(request):
    return register_user(request, HODRegistrationForm, 'HOD', 'register_hod.html', 'hod_dashboard')

def register_staff(request):
    return register_user(request, StaffRegistrationForm, 'Staff', 'register_staff.html', 'staff_dashboard')

def register_principal(request):
    return register_user(request, PrincipalRegistrationForm, 'Principal', 'register_principal.html', 'principal_dashboard')


@login_required
def success(request):   
    return render(request, 'success.html')

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page or wherever you want
    else:
        form = TeacherRegistrationForm()
    
    return render(request, 'register_teacher.html', {'form': form})
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
        'courses': getattr(profile, 'courses', None)  # Assumes ManyToManyField for Student
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

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AttendanceForm
from .models import Teacher, Course, Student, Attendance

@login_required
def mark_attendance(request):
    # Check if user is in 'Teacher' group
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect('no_permission')

    # Retrieve the teacher
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect('no_permission')

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data.get('course')
            students = Student.objects.filter(courses_taught=course)
            
            # Ensure all students for the selected course are marked
            for student in students:
                attendance_status = request.POST.get(f'student_{student.id}')
                if attendance_status:
                    Attendance.objects.update_or_create(
                        student=student,
                        date=form.cleaned_data.get('date'),
                        defaults={'status': attendance_status, 'teacher': teacher}
                    )
                    
            messages.success(request, "Attendance successfully marked.")
            return redirect('success')
        else:
            messages.error(request, "There was an error in the form. Please check your input.")
    else:
        form = AttendanceForm()

    courses = Course.objects.filter(teachers=teacher)
    return render(request, 'mark_attendance.html', {'form': form, 'courses': courses})


@login_required
def no_permission(request):
    return render(request, 'no_permission.html')

def view_grades(request):
    if not request.user.groups.filter(name='Student').exists():
        return redirect('no_permission')

    student_profile = Student.objects.get(user=request.user)
    grades = student_profile.grades.all()  # Assuming Student has related grades

    return render(request, 'view_grades.html', {'grades': grades})

from django.shortcuts import render
from django.db.models import Q

def principal_view(request):
    # Retrieve query parameters
    department_id = request.GET.get('department', '')
    semester_id = request.GET.get('semester', '')
    honors_minors_id = request.GET.get('honors_minors', '')
    status = request.GET.get('status', '')
    search_query = request.GET.get('search', '')

    # Base query: Get all students
    students = Student.objects.all()

    # Filter by department
    if department_id:
        students = students.filter(department_id=department_id)

    # Filter by semester (handling both EvenSem and OddSem)
    if semester_id:
        students = students.filter(
            Q(even_sem__id=semester_id) | Q(odd_sem__id=semester_id)
        )

    # Filter by Honors/Minors
    if honors_minors_id:
        students = students.filter(honors_minors_id=honors_minors_id)

    # Filter by status (make sure to verify that 'status' exists in the model)
    if status:
        students = students.filter(status=status)

    # Search across name and user fields
    if search_query:
        students = students.filter(
            Q(user__username__icontains=search_query) | 
            Q(user__first_name__icontains=search_query) | 
            Q(user__last_name__icontains=search_query)
        )

    # Fetch relevant data for filtering in the template
    departments = Department.objects.all()
    all_semesters = Semester.objects.all()
    honors_minors = HonorsMinors.objects.all()
    statuses = Student.objects.values_list('status', flat=True).distinct()

    # Prepare the context for rendering
    context = {
        'students': students,
        'departments': departments,
        'all_semesters': all_semesters,
        'honors_minors': honors_minors,
        'statuses': statuses
    }

    # Handle AJAX request (if any)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'student_table_rows.html', context)

    # Render the full principal page
    return render(request, 'principal.html', context)

def index(request):
    return render(request, 'index.html')





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

@login_required
def dash_teacher(request):
    return render(request, 'dash_teacher.html')

def demo_dash(request):
    return render(request, 'demo_dash.html')
    
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



@login_required
def principal_dashboard(request):
    if not request.user.groups.filter(name='Principal').exists():
        return redirect('no_permission')  # Redirect to a page showing no permission message

    # Fetch principal's department
    principal_profile = Principal.objects.get(user=request.user)
    department = principal_profile.department

    # Example of fetching data
    teachers = Teacher.objects.filter(department=department)

    return render(request, 'principal_dashboard.html', {'department': department, 'teachers': teachers})

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

    hod_profile = HOD.objects.get(user=request.user)
    department = hod_profile.department

    # Fetch department-specific data
    teachers = Teacher.objects.filter(department=department)
    students = Student.objects.filter(department=department)

    return render(request, 'hod_dashboard.html', {'department': department, 'teachers': teachers, 'students': students})

from django.shortcuts import get_object_or_404, redirect
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

    staff_profile = Staff.objects.get(user=request.user)
    department = staff_profile.assigned_department

    # Example of fetching department-specific data
    students = Student.objects.filter(department=department)

    return render(request, 'staff_dashboard.html', {'department': department, 'students': students})

@login_required
def view_student_details(request):
    
    if not (request.user.groups.filter(name='Staff').exists() or request.user.groups.filter(name='HOD').exists() or request.user.groups.filter(name='Principal').exists()):
        return redirect('no_permission')

    staff_profile = Staff.objects.get(user=request.user)
    department = staff_profile.assigned_department
    students = Student.objects.filter(department=department)

    return render(request, 'view_student_details.html', {'students': students})

@login_required
def student_dashboard(request):
    if not request.user.groups.filter(name='Student').exists():
        return redirect('no_permission')

    student_profile = Student.objects.get(user=request.user)
    department = student_profile.department
    
    # Fetch student's enrolled courses
    courses = student_profile.courses.all()  # Use `courses` if it's a ManyToManyField

    return render(request, 'student_dashboard.html', {'department': department, 'courses': courses})



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




from django.shortcuts import render

def dashboard(request):
    # Fetch the department, teachers, students, and courses from your models as needed
    department = request.user.department if hasattr(request.user, 'department') else None
    teachers = department.teacher_set.all() if department else None
    students = department.student_set.all() if department else None
    courses = request.user.courses.all() if hasattr(request.user, 'courses') else None

    # Check user roles and pass boolean values to the context
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
