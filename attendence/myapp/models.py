from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Permission, ContentType

class CustomUser(AbstractUser):
    PRINCIPAL = 'principal'
    HOD = 'hod'
    TEACHER = 'teacher'
    STUDENT = 'student'
    STAFF = 'staff'

    ROLE_CHOICES = [
        (PRINCIPAL, 'Principal'),
        (HOD, 'HOD'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
        (STAFF, 'Staff'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Principal(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    office_location = models.CharField(max_length=255, default="Unknown Location")
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        permissions = [
            ("can_view_principal", "Can view principal details"),
        ]

    def __str__(self):
        return f"Principal: {self.user.username} - Department: {self.department.name if self.department else 'No Department'}"

class HOD(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, default=None)
    office_number = models.CharField(max_length=50, default="Unknown")
    managing_teachers = models.IntegerField(default=0)

    class Meta:
        permissions = [
            ("can_view_hod", "Can view HOD details"),
        ]

    def __str__(self):
        return f"HOD: {self.user.username} - {self.department.name if self.department else 'No Department'}"

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, default=None)
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True, default=None)
    courses_taught = models.ManyToManyField('Course', blank=True)
    faculty_id = models.CharField(max_length=10, unique=True, default="UNKNOWN")

    class Meta:
        permissions = [
            ("can_view_teacher", "Can view teacher details"),
        ]

    def __str__(self):
        return f"Teacher: {self.user.username} - Department: {self.department.name if self.department else 'No Department'}"

class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, default="Unknown Position")
    assigned_department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, default=None)
    staff_id = models.CharField(max_length=10, unique=True, default="UNKNOWN")

    class Meta:
        permissions = [
            ("can_view_staff", "Can view staff details"),
        ]

    def __str__(self):
        return f"Staff: {self.user.username} - Position: {self.position}"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, default=None)
    roll_number = models.CharField(max_length=10, unique=True, null=True, blank=True, default=None)
    odd_sem = models.ForeignKey('OddSem', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    even_sem = models.ForeignKey('EvenSem', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    year_of_study = models.CharField(max_length=4, default="2024")
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    class Meta:
        permissions = [
            ("can_view_student", "Can view student details"),
        ]

    def __str__(self):
        return f"Student: {self.user.username} - Roll No: {self.roll_number if self.roll_number else 'No Roll Number'}"

# Continue with other models, adding permissions as needed

class Year(models.Model):
    name = models.CharField(max_length=100, default="Unknown Year")

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, default="Unknown Course")
    code = models.CharField(max_length=10, unique=True, default="UNKNOWN")

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, default="Unknown Department")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

class HonorsMinors(models.Model):
    name = models.CharField(max_length=100, default="Unknown Honors/Minors")
    even_sem = models.ForeignKey('EvenSem', on_delete=models.CASCADE, default=None)
    odd_sem = models.ForeignKey('OddSem', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name
    
class EvenSem(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None)
    program = models.ForeignKey('Program', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Even Sem {self.id} - {self.department.name if self.department else 'No Department'}"

class OddSem(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None)
    program = models.ForeignKey('Program', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Odd Sem {self.id} - {self.department.name if self.department else 'No Department'}"

class Program(models.Model):
    name = models.CharField(max_length=100, default="Unknown Program")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None)
    semester = models.CharField(max_length=10, default="Unknown Semester")

    def __str__(self):
        return f"{self.name} - {self.semester}"

class Lecture(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Lecture for {self.program.name if self.program else 'Unknown Program'} - Student {self.student.user.username if self.student else 'Unknown Student'}"

class LabsBatches(models.Model):
    name = models.CharField(max_length=100, default="Unknown Lab Batch")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, default=None)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Lab Batch {self.name} - Program {self.program.name if self.program else 'Unknown Program'}"
