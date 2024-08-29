from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from control_system.models import Student, Teacher, Principal

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST.get('user_type')  # Get the user type from the login form

        # Check the user type and find the corresponding user
        user = None
        if user_type == 'STUDENT':
            user = Student.objects.filter(username=username).first()
        elif user_type == 'TEACHER':
            user = Teacher.objects.filter(username=username).first()
        elif user_type == 'PRINCIPAL':
            user = Principal.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            # Manually create a session for the user
            request.session['user_id'] = user.id
            request.session['user_type'] = user_type
            request.session['username'] = username

            if user_type == 'STUDENT':
                return redirect('student_dashboard')
            elif user_type == 'TEACHER':
                return redirect('teacher_dashboard')
            elif user_type == 'PRINCIPAL':
                return redirect('principal_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

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

def done(request):
    return render(request, 'done.html')

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from control_system.models import Student, Teacher, Principal
from .forms import UserForm

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            
            hashed_password = make_password(password)

            if user_type == 'STUDENT':
                Student.objects.create(username=username, password=hashed_password)
            elif user_type == 'TEACHER':
                Teacher.objects.create(username=username, password=hashed_password)
            elif user_type == 'PRINCIPAL':
                Principal.objects.create(username=username, password=hashed_password)

            return redirect('done')  # Redirect to a success page or wherever you prefer
    else:
        form = UserForm()

    return render(request, 'add_user.html', {'form': form})
