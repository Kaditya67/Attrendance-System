from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields if needed

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields if needed

class Principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields if needed
