from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from control_system.models import Student, Teacher, Principal
from .forms import UserForm  # The form for adding users

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']

            user = None
            if user_type == 'STUDENT':
                user = Student.objects.create(username=username, password=password)
            elif user_type == 'TEACHER':
                user = Teacher.objects.create(username=username, password=password)
            elif user_type == 'PRINCIPAL':
                user = Principal.objects.create(username=username, password=password)
            
            # Automatically log in the user
            request.session['user_type'] = user_type
            request.session['username'] = username  # Store username in session
            return redirect('done')

    else:
        form = UserForm()

    return render(request, 'add_user.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from control_system.models import Student, Teacher, Principal
from .forms import UserLoginForm  # The form for logging in users

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']

            user = None
            if user_type == 'STUDENT':
                user = Student.objects.filter(username=username).first()
            elif user_type == 'TEACHER':
                user = Teacher.objects.filter(username=username).first()
            elif user_type == 'PRINCIPAL':
                user = Principal.objects.filter(username=username).first()

            if user and check_password(password, user.password):
                request.session['user_type'] = user_type
                request.session['username'] = username  # Store username in session
                return redirect(f'{user_type.lower()}_dashboard')  # Redirect to dashboard
            else:
                form.add_error(None, 'Invalid username or password')

    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def student_dashboard(request):
    if request.session.get('user_type') != 'STUDENT':
        return redirect('login')
    return render(request, 'student_dashboard.html')

@login_required
def teacher_dashboard(request):
    if request.session.get('user_type') != 'TEACHER':
        return redirect('login')
    return render(request, 'teacher_dashboard.html')

@login_required
def principal_dashboard(request):
    if request.session.get('user_type') != 'PRINCIPAL':
        return redirect('login')
    return render(request, 'principal_dashboard.html')

def success_page(request):
    return render(request, 'done.html')