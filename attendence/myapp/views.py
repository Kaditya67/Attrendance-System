from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegistrationForm

from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm

# def register_student(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('student_dashboard')  # Redirect to a success page or another view
#     else:
#         form = StudentRegistrationForm()

#     return render(request, 'register_student.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AttendanceForm
from .models import EvenSem, HonorsMinors, OddSem, Principal, Teacher, Department, Student, HOD, Staff

from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import UserRegistrationForm, UserLoginForm
from .models import Profile

# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm, UserLoginForm
from .models import Profile
# from .utils import create_or_update_teacher

# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm, UserLoginForm
from .models import Profile
# from .utils import create_or_update_teacher

# views.py
from django.shortcuts import render, redirect
from .forms import TeacherRegistrationForm

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
    
    return render(request, 'teacher_register.html', {'form': form})


# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from .forms import HODRegistrationForm, StaffRegistrationForm, PrincipalRegistrationForm
from .models import HOD, Staff, Principal

# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as auth_login
from .forms import HODRegistrationForm, StaffRegistrationForm, PrincipalRegistrationForm
from .models import HOD, Staff, Principal

from django.shortcuts import render, redirect
from .forms import HODRegistrationForm

def register_hod(request):
    if request.method == 'POST':
        form = HODRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Replace with your success URL
    else:
        form = HODRegistrationForm()
    return render(request, 'register_hod.html', {'form': form})


# views.py
from django.shortcuts import render, redirect
from .forms import StaffRegistrationForm

def register_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = StaffRegistrationForm()
    return render(request, 'register_staff.html', {'form': form})


def register_principal(request):
    if request.method == 'POST':
        form = PrincipalRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auth_login(request, user)
            return redirect('success')  # Replace with your success URL
    else:
        form = PrincipalRegistrationForm()

    return render(request, 'register_principal.html', {'form': form})

def dash_teacher(request):
    return render(request, 'dash_teacher.html')

def demo_dash(request):
    return render(request, 'demo_dash.html')
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


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# views.py
from django.shortcuts import render

def success(request):
    return render(request, 'success.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AttendanceForm
from .models import Teacher

@login_required
def mark_attendance(request):
    if not request.user.groups.filter(name='Teacher').exists():
        return redirect('no_permission')  # Redirect to a page showing no permission message
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.teacher = Teacher.objects.get(user=request.user)
            attendance.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = AttendanceForm()

    return render(request, 'mark_attendance.html', {'form': form})



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

@login_required
def manage_teachers(request):
    if not request.user.groups.filter(name='HOD').exists():
        return redirect('no_permission')

    hod_profile = HOD.objects.get(user=request.user)
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
    if not request.user.groups.filter(name='Staff').exists():
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
    # Fetch student's details
    courses = student_profile.courses_taught.all()  # Assuming Student has related courses

    return render(request, 'student_dashboard.html', {'department': department, 'courses': courses})


@login_required
def no_permission(request):
    return render(request, 'no_permission.html')

@login_required
def view_grades(request):
    if not request.user.groups.filter(name='Student').exists():
        return redirect('no_permission')

    student_profile = Student.objects.get(user=request.user)
    grades = student_profile.grades.all()  # Assuming Student has related grades

    return render(request, 'view_grades.html', {'grades': grades})


def principal(request):
    # Fetch query parameters for filtering
    department_id = request.GET.get('department', '')
    semester_id = request.GET.get('semester', '')
    honors_minors_id = request.GET.get('honors_minors', '')
    status = request.GET.get('status', '')
    search_query = request.GET.get('search', '')

    # Start with all students
    students = Student.objects.all()

    if department_id:
        students = students.filter(department_id=department_id)
    if semester_id:
        even_sem = EvenSem.objects.filter(id=semester_id).first()
        odd_sem = OddSem.objects.filter(id=semester_id).first()
        students = students.filter(even_sem=even_sem) | students.filter(odd_sem=odd_sem)
    if honors_minors_id:
        students = students.filter(honors_minors_id=honors_minors_id)
    if status:
        students = students.filter(status=status)
    if search_query:
        students = students.filter(name__icontains=search_query)

    # Fetch other data for the dropdowns
    departments = Department.objects.all()
    even_sems = EvenSem.objects.all()
    odd_sems = OddSem.objects.all()
    honors_minors = HonorsMinors.objects.all()
    statuses = Student.objects.values_list('status', flat=True).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Return HTML snippet for the table rows only
        context = {
            'students': students,
        }
        return render(request, 'student_table_rows.html', context)

    context = {
        'students': students,
        'departments': departments,
        'all_semesters': list(even_sems) + list(odd_sems),
        'honors_minors': honors_minors,
        'statuses': statuses,
    }

    return render(request, 'principal.html', context)



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


def dashboard(request):   
    return render(request, 'dashboard.html')

def index(request):
    return render(request, 'index.html')