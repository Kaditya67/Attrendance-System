from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    user_type = forms.ChoiceField(choices=[('STUDENT', 'Student'), ('TEACHER', 'Teacher'), ('PRINCIPAL', 'Principal')], required=True)
