from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db import transaction
from .models import Student, Department, Teacher, HOD, Staff, Principal, Course, Attendance, Semester
from django.contrib.auth import authenticate

<<<<<<< HEAD
=======
from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'lab_batch', 'date', 'time_slot', 'present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

>>>>>>> c22b95e10b9996e1ebc994b1a1dbe55c94ce1b4d

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
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            self.user = user  # Save the authenticated user

        return cleaned_data

    def get_user(self):
        return self.user

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Student, Department
class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(validators=[EmailValidator(message="Enter a valid email address ending with @dbit.in")])
    mobile_no = forms.CharField(max_length=15, required=False)
<<<<<<< HEAD
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'onchange': 'updateSemesters()'}))
=======
    # department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'onchange': 'updateSemesters()'}))
>>>>>>> c22b95e10b9996e1ebc994b1a1dbe55c94ce1b4d
    roll_number = forms.CharField(max_length=10)
    student_id = forms.CharField(max_length=20, required=True, label="Student ID")  # Added student_id
    address = forms.CharField(widget=forms.Textarea, required=False, label="Address")  # Added address
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), required=False)  # Show all semesters

    class Meta:
        model = Student
        fields = [
            'username', 'first_name', 'last_name', 'email', 'mobile_no',
<<<<<<< HEAD
            'department', 'roll_number', 'student_id', 'address', 
=======
            # 'department', 
            'roll_number', 'student_id', 'address', 
>>>>>>> c22b95e10b9996e1ebc994b1a1dbe55c94ce1b4d
            'password', 'confirm_password', 'semester'
        ]
        help_texts = {
            'email': 'Enter a valid email address ending with @dbit.in',
        }

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
from .models import Student

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'address']
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set other fields as disabled
        for field in self.fields:
            if field not in ['roll_number', 'address']:
                self.fields[field].widget.attrs['disabled'] = 'disabled'


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
        help_texts = {
            'faculty_id': 'Unique ID assigned to the faculty member.',
        }

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
        help_texts = {
            'department': 'The department this HOD manages.',
            'managing_teachers': 'Number of teachers this HOD manages.'
        }

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
        help_texts = {
            'position': 'The staff position or role.',
            'staff_id': 'Unique ID assigned to the staff member.'
        }

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
        help_texts = {
            'office_location': 'The location of the principal’s office.',
        }

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

class AttendanceForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label='Select Course')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Attendance Date')

    def __init__(self, *args, **kwargs):
        teacher_courses = kwargs.pop('teacher_courses', None)
        super().__init__(*args, **kwargs)
        if teacher_courses:
            self.fields['course'].queryset = teacher_courses
        else:
            self.fields['course'].queryset = Course.objects.none()  # No courses available if no teacher_courses provided



# Extra features form

from django import forms
from .models import Enrollment, Course, Student, Semester

class CourseEnrollmentForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label='Select Course')
    semester = forms.ModelChoiceField(queryset=Semester.objects.none(), label='Select Semester')

    class Meta:
        model = Enrollment
        fields = ['course', 'semester']

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['course'].queryset = Course.objects.filter(department=student.department)
            self.fields['semester'].queryset = Semester.objects.filter(session_year__department=student.department)


from django import forms
from .models import Course, Department, Year

class CourseManagementForm(forms.ModelForm):
    code = forms.CharField(max_length=10)
    name = forms.CharField(max_length=100)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    year = forms.ModelChoiceField(queryset=Year.objects.all())

    class Meta:
        model = Course
        fields = ['code', 'name', 'department', 'year']


<<<<<<< HEAD
from django import forms
from .models import Lecture, Course, Semester, Program

class LectureSchedulingForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Select Course')
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label='Select Semester')
    program = forms.ModelChoiceField(queryset=Program.objects.all(), label='Select Program')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date')
    time_slot = forms.ChoiceField(choices=Lecture.TIME_SLOT_CHOICES, label='Time Slot')

    class Meta:
        model = Lecture
        fields = ['course', 'semester', 'program', 'date', 'time_slot']
=======
# from django import forms
# from .models import Lecture, Course, Semester, Program

# class LectureSchedulingForm(forms.ModelForm):
#     course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Select Course')
#     semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label='Select Semester')
#     program = forms.ModelChoiceField(queryset=Program.objects.all(), label='Select Program')
#     date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='Date')
#     time_slot = forms.ChoiceField(choices=Lecture.TIME_SLOT_CHOICES, label='Time Slot')

#     class Meta:
#         model = Lecture
#         fields = ['course', 'semester', 'program', 'date', 'time_slot']
>>>>>>> c22b95e10b9996e1ebc994b1a1dbe55c94ce1b4d


from django import forms
from .models import Attendance, Course

class AttendanceReportForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Select Course')
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='From Date')
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='To Date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()


from django import forms
from .models import Student

# class StudentProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['email', 'mobile_no', 'address', 'cgpa']
#         widgets = {
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'class': 'form-control'}),
#             'cgpa': forms.NumberInput(attrs={'class': 'form-control'})
#         }


from django import forms
from .models import Teacher

class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['email', 'mobile_no', 'experience']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control'}),
        }


from django import forms
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

from django import forms
from .models import Student

# class StudentProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_id', 'department', 'roll_number', 'semester', 'year', 'cgpa', 'mobile_no', 'email', 'address', 'courses', 'lab_batch']
#         widgets = {
#             'courses': forms.CheckboxSelectMultiple,
#             'lab_batch': forms.Select,
#         }

from django import forms
from .models import Student

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_id', 'department', 'roll_number', 'semester', 'year', 'cgpa', 'mobile_no', 'email', 'address', 'courses', 'lab_batch']
#         widgets = {
#             'courses': forms.CheckboxSelectMultiple,
#             'lab_batch': forms.Select,
#         }

from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name']


from django import forms
from .models import Lecture, Course, Program, Semester

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['program', 'course', 'semester', 'date', 'time_slot']
