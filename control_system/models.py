from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    # Add other fields if needed

    def __str__(self):
        return self.username


class Teacher(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    # Add other fields if needed

    def __str__(self):
        return self.username


class Principal(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    # Add other fields if needed

    def __str__(self):
        return self.username
