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
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='STUDENT', verbose_name="User Type")

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

    class Meta:
        indexes = [
            models.Index(fields=['user_type']),
        ]

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Department Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class SessionYear(models.Model):
    academic_year = models.CharField(max_length=10, verbose_name="Academic Year")  # e.g., "2023-2024"
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sessions', verbose_name="Department")

    def __str__(self):
        return f"{self.academic_year} - {self.department.name}"

    class Meta:
        indexes = [
            models.Index(fields=['academic_year']),
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]

class Year(models.Model):
    YEAR_CHOICES = [
        ('FE', 'First Year'),
        ('SE', 'Second Year'),
        ('TE', 'Third Year'),
        ('BE', 'Fourth Year'),
    ]
    name = models.CharField(max_length=10, choices=YEAR_CHOICES, verbose_name="Year")

    def __str__(self):
        return self.get_name_display()

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Course Code")
    name = models.CharField(max_length=100, verbose_name="Course Name")
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, related_name='course_list', verbose_name="Semester",blank=True, null=True)  # Change related_name
    is_lab = models.BooleanField(default=False, verbose_name="Is Lab")
    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
        ]

class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('Odd', 'Odd'),
        ('Even', 'Even'),
    ]
    
    YEAR_CHOICES = [
        ('FE', 'First Year'),
        ('SE', 'Second Year'),
        ('TE', 'Third Year'),
        ('BE', 'Fourth Year'),
    ]

    semester_number = models.IntegerField(verbose_name="Semester Number")
    session_year = models.ForeignKey(SessionYear, on_delete=models.CASCADE, related_name='semesters', verbose_name="Session Year")
    semester_type = models.CharField(max_length=10, choices=SEMESTER_CHOICES, verbose_name="Semester Type")
    year = models.CharField(max_length=2, choices=YEAR_CHOICES, verbose_name="Year")

    courses = models.ManyToManyField(Course, related_name='semesters', verbose_name="Courses", blank=True)

    class Meta:
        unique_together = ('session_year', 'semester_number')
        indexes = [
            models.Index(fields=['semester_number']),
            models.Index(fields=['semester_type']),
        ]

    def __str__(self):
        return f"{self.get_semester_type_display()} Sem {self.semester_number} - {self.session_year.department.name}"



class Program(models.Model):
    name = models.CharField(max_length=100, verbose_name="Program Name")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs', verbose_name="Department")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='programs', verbose_name="Year", blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.department.name}"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class HonorsMinors(models.Model):
    name = models.CharField(max_length=100, verbose_name="Honors/Minors Name")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='honors_minors', null=True, blank=True, verbose_name="Semester")

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class LabsBatches(models.Model):
    name = models.CharField(max_length=100, verbose_name="Batch Name")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='labs_batches', verbose_name="Program")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='labs_batches', verbose_name="Department")

    def __str__(self):
        return f"Lab Batch {self.name} - Program {self.program.name}"

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers', verbose_name="Department")
    courses_taught = models.ManyToManyField(Course, blank=True, related_name='teachers', verbose_name="Courses Taught")
    faculty_id = models.CharField(max_length=10, unique=True, verbose_name="Faculty ID")
    mobile_no = models.CharField(max_length=15, blank=True, null=True, verbose_name="Mobile Number")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    experience = models.TextField(blank=True, null=True, verbose_name="Experience")
    assigned_courses = models.ManyToManyField(Course, related_name='assigned_teachers', verbose_name="Assigned Courses", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['faculty_id']),
            models.Index(fields=['mobile_no']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"Teacher: {self.user.username} - Department: {self.department.name if self.department else 'No Department'}"


class HOD(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE) 
    office_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Office Number")
    managing_teachers = models.IntegerField(verbose_name="Managing Teachers")

    def __str__(self):
        return self.teacher.user.get_full_name()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Student ID")
    roll_number = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name="Roll Number")
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name="Semester")
    mobile_no = models.CharField(max_length=15, blank=True, null=True, verbose_name="Mobile Number")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    lab_batch = models.ForeignKey(LabsBatches, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lab Batch")

    def calculate_attendance_percentage(self):
        total_classes = self.attendances.count()
        attended_classes = self.attendances.filter(present=True).count()
        if total_classes > 0:
            return (attended_classes / total_classes) * 100
        return 0

    def __str__(self):
        return f"Student: {self.user.username} - ID: {self.student_id} - Roll No: {self.roll_number}"

    class Meta:
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['roll_number']),
            models.Index(fields=['email']),
        ]


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Course")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Semester")

    class Meta:
        unique_together = ('student', 'course', 'semester')
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['course']),
            models.Index(fields=['semester']),
        ]

    def __str__(self):
        return f"Enrollment: {self.student.user.username} in {self.course.name} - {self.semester}"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, verbose_name="Position")
    assigned_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff', verbose_name="Assigned Department")
    staff_id = models.CharField(max_length=10, unique=True, verbose_name="Staff ID")

    def __str__(self):
        return f"Staff: {self.user.username} - Position: {self.position}"

    class Meta:
        indexes = [
            models.Index(fields=['staff_id']),
        ]

class Principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office_location = models.CharField(max_length=255, default="Unknown Location", verbose_name="Office Location")

    class Meta:
        permissions = [
            ("can_view_principal", "Can view Principal details"),
        ]
        indexes = [
            models.Index(fields=['office_location']),
        ]

    def __str__(self):
        return f"Principal: {self.user.username} - Office: {self.office_location}"

from django.db import models

# Shared constant for time slot choices
TIME_SLOT_CHOICES = [
    ('8-9', '8:00 AM - 9:00 AM'),
    ('9-10', '9:00 AM - 10:00 AM'),
    ('10-11', '10:00 AM - 11:00 AM'),
    ('11:15-12:15', '11:15 AM - 12:15 PM'),
    ('12:15-1:15', '12:15 PM - 1:15 PM'),
    ('2-3', '2:00 PM - 3:00 PM'),
    ('3-4', '3:00 PM - 4:00 PM'),
    ('4-5', '4:00 PM - 5:00 PM'),
]
class Lecture(models.Model):
    # Define the choices for time slots
    TIME_SLOT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='lectures', verbose_name="Program")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', verbose_name="Course")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='lectures', verbose_name="Semester")
    date = models.DateField(verbose_name="Date")
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES, verbose_name="Time Slot")
    
    def __str__(self):
        return f"Lecture on {self.date} for {self.course.name} - {self.program.name} ({self.get_time_slot_display()})"

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['time_slot']),
            models.Index(fields=['date', 'time_slot']),  # Compound index for faster querying
        ]

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances', verbose_name="Course")
    lab_batch = models.ForeignKey(LabsBatches, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lab Batch")
    date = models.DateField(verbose_name="Date")
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES, verbose_name="Time Slot", null=True, blank=True)
    present = models.BooleanField(default=False, verbose_name="Present")
    count = models.IntegerField(default=0, verbose_name="Count", null=True, blank=True)

    # Optional: Additional fields
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")  # Optional notes field
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)  # Timestamp when the record is created
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)  # Timestamp when the record is updated

    def __str__(self):
        return f"Attendance: {self.student.user.username} - {self.course.name} - {self.date} - {'Present' if self.present else 'Absent'}"

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['present']),
     
        models.Index(fields=['date', 'time_slot']),  # Compound index for faster querying
        ]
        unique_together = ('student', 'course', 'date', 'lab_batch')  # Unique constraint



class SemesterCGPA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='semester_cgpas', verbose_name="Student")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='semester_cgpas', verbose_name="Semester")
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="CGPA")

    class Meta:
        unique_together = ('student', 'semester')
        indexes = [
            models.Index(fields=['semester']),
            models.Index(fields=['cgpa']),
        ]

    def __str__(self):
        return f"CGPA for {self.semester} - {self.student.user.username}: {self.cgpa}"