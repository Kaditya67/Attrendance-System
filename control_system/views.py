from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
from .models import Student, Teacher, Principal

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Redirect based on the selected role
                if role == 'student' and Student.objects.filter(user=user).exists():
                    return redirect('student_dashboard')
                elif role == 'teacher' and Teacher.objects.filter(user=user).exists():
                    return redirect('teacher_dashboard')
                elif role == 'principal' and Principal.objects.filter(user=user).exists():
                    return redirect('principal_dashboard')
                else:
                    # If role is not found in database, redirect to login with error
                    return render(request, 'login.html', {'form': form, 'error': 'Invalid role or not assigned.'})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
def principal_dashboard(request):
    return render(request, 'principal_dashboard.html')
