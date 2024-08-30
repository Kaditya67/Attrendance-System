from django import forms
from django.contrib.auth.hashers import check_password

from .models import Student, Teacher, Principal


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    user_type = forms.ChoiceField(
        choices=[('STUDENT', 'Student'), ('TEACHER', 'Teacher'), ('PRINCIPAL', 'Principal')],
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user_type = cleaned_data.get('user_type')

        if username and password and user_type:
            user = None
            if user_type == 'STUDENT':
                from control_system.models import Student
                user = Student.objects.filter(username=username).first()
            elif user_type == 'TEACHER':
                from control_system.models import Teacher
                user = Teacher.objects.filter(username=username).first()
            elif user_type == 'PRINCIPAL':
                from control_system.models import Principal
                user = Principal.objects.filter(username=username).first()

            if user and not check_password(password, user.password):
                self.add_error('password', 'Incorrect password')
            elif not user:
                self.add_error('username', 'Username does not exist')

        return cleaned_data
