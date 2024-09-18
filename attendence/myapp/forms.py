from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db import transaction
from .models import Student, Department

from django import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        label='Password'
    )

    def __init__(self, *args, **kwargs):
        self.user = None  # Store the authenticated user
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            # Use Django's authenticate function to check user credentials
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            self.user = user  # Save the authenticated user

        return cleaned_data

    def get_user(self):
        return self.user


class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(validators=[EmailValidator(message="Enter a valid email address ending with @dbit.in")])
    mobile_no = forms.CharField(max_length=15, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    roll_number = forms.CharField(max_length=10)
    year_of_study = forms.IntegerField()
    cgpa = forms.DecimalField(max_digits=4, decimal_places=2, initial=0.00)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Student
        fields = [
            'username', 'first_name', 'last_name', 'email', 'mobile_no',
            'department', 'roll_number', 'year_of_study', 'cgpa', 'password', 'confirm_password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@dbit.in'):
            raise ValidationError("Email must end with @dbit.in")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        
        student = super().save(commit=False)
        student.user = user
        
        if commit:
            student.save()
        return student

from django import forms
from django.contrib.auth.models import User
from .models import Teacher, Department, Course

class TeacherRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    mobile_no = forms.CharField(max_length=15, required=False)
    email = forms.EmailField()
    experience = forms.CharField(widget=forms.Textarea, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    courses_taught = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), required=False)
    faculty_id = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Teacher
        fields = ['username', 'first_name', 'last_name', 'mobile_no', 'email', 'experience', 'department',
                    'courses_taught', 'faculty_id', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.is_staff = True  # Mark user as staff
        user.save()
        
        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
            self.save_m2m()  # Save many-to-many fields
        return teacher


from django import forms
from django.contrib.auth.models import User
from .models import HOD, Department

class HODRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    office_number = forms.CharField(max_length=50, required=False)
    managing_teachers = forms.IntegerField(required=False)

    class Meta:
        model = HOD
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'department', 'office_number', 'managing_teachers']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.is_staff = True  # Mark user as staff
        user.save()
        
        hod = super().save(commit=False)
        hod.user = user
        if commit:
            hod.save()
        return hod

from django import forms
from django.contrib.auth.models import User
from .models import Staff, Department

class StaffRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    position = forms.CharField(max_length=100, required=False)
    assigned_department = forms.ModelChoiceField(queryset=Department.objects.all())
    staff_id = forms.CharField(max_length=10)

    class Meta:
        model = Staff
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'position', 'assigned_department', 'staff_id']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.is_staff = True  # Mark user as staff
        user.save()
        
        staff = super().save(commit=False)
        staff.user = user
        if commit:
            staff.save()
        return staff

from django import forms
from django.contrib.auth.models import User
from .models import Principal, Department

class PrincipalRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    office_location = forms.CharField(max_length=255, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = Principal
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'office_location', 'department']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.is_staff = True  # Mark user as staff
        user.save()
        
        principal = super().save(commit=False)
        principal.user = user
        if commit:
            principal.save()
        return principal


from django import forms
from .models import Attendance

from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(choices=Attendance.STATUS_CHOICES, attrs={'class': 'form-control'})
        }
        labels = {
            'student': 'Select Student',
            'date': 'Attendance Date',
            'status': 'Attendance Status'
        }
