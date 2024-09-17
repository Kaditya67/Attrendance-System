# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
        ('STAFF', 'Staff'),
        ('HOD', 'HOD'),
        ('PRINCIPAL', 'Principal'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Department(models.Model):
    name = models.CharField(max_length=100, default="Unknown Department")
    year = models.ForeignKey('Year', on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

class Year(models.Model):
    name = models.CharField(max_length=100, default="Unknown Year")

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, default="Unknown Course")
    code = models.CharField(max_length=10, unique=True, default="UNKNOWN")

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=100, default="Unknown Program")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='programs')
    semester = models.CharField(max_length=10, default="Unknown Semester")

    def __str__(self):
        return f"{self.name} - {self.semester}"

class EvenSem(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='even_sems')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='even_sems')

    def __str__(self):
        return f"Even Sem {self.id} - {self.department.name if self.department else 'No Department'}"

class OddSem(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='odd_sems')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='odd_sems')

    def __str__(self):
        return f"Odd Sem {self.id} - {self.department.name if self.department else 'No Department'}"

class HonorsMinors(models.Model):
    name = models.CharField(max_length=100, default="Unknown Honors/Minors")
    even_sem = models.ForeignKey(EvenSem, on_delete=models.CASCADE, related_name='honors_minors')
    odd_sem = models.ForeignKey(OddSem, on_delete=models.CASCADE, related_name='honors_minors')

    def __str__(self):
        return self.name

class LabsBatches(models.Model):
    name = models.CharField(max_length=100, default="Unknown Lab Batch")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='labs_batches')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='labs_batches')

    def __str__(self):
        return f"Lab Batch {self.name} - Program {self.program.name if self.program else 'Unknown Program'}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    courses_taught = models.ManyToManyField(Course, blank=True)
    faculty_id = models.CharField(max_length=10, unique=True, default="UNKNOWN")
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)

    class Meta:
        permissions = [
            ("can_view_student_data", "Can view student data"),
        ]

    def __str__(self):
        return f"Teacher: {self.user.username} - Department: {self.department.name if self.department else 'No Department'}"

# models.py

from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    roll_number = models.CharField(max_length=10, unique=True, null=True, blank=True, default=None)
    odd_sem = models.ForeignKey('OddSem', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    even_sem = models.ForeignKey('EvenSem', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    year_of_study = models.CharField(max_length=4, default="2024")
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        permissions = [
            ("can_view_student", "Can view student details"),
        ]

    def __str__(self):
        return f"Student: {self.user.username} - Roll No: {self.roll_number if self.roll_number else 'No Roll Number'}"

class HOD(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='hods')
    office_number = models.CharField(max_length=50, default="Unknown")
    managing_teachers = models.IntegerField(default=0)

    class Meta:
        permissions = [
            ("can_view_hod", "Can view HOD details"),
        ]

    def __str__(self):
        return f"HOD: {self.user.username} - {self.department.name if self.department else 'No Department'}"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, default="Unknown Position")
    assigned_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    staff_id = models.CharField(max_length=10, unique=True, default="UNKNOWN")

    class Meta:
        permissions = [
            ("can_view_staff", "Can view staff details"),
        ]

    def __str__(self):
        return f"Staff: {self.user.username} - Position: {self.position}"

class Principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office_location = models.CharField(max_length=255, default="Unknown Location")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='principals')

    class Meta:
        permissions = [
            ("can_view_principal", "Can view Principal details"),
        ]

    def __str__(self):
        return f"Principal: {self.user.username} - Department: {self.department.name if self.department else 'No Department'}"

class Lecture(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='lectures')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lectures')

    def __str__(self):
        return f"Lecture for {self.program.name if self.program else 'Unknown Program'} - Student {self.student.user.username if self.student else 'Unknown Student'}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField()

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {'Present' if self.is_present else 'Absent'}"
