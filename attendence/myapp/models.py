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

class Year(models.Model):
    YEAR_CHOICES = [
        ('FE', 'First Year'),
        ('SE', 'Second Year'),
        ('TE', 'Third Year'),
        ('BE', 'Fourth Year'),
    ]
    name = models.CharField(max_length=10, choices=YEAR_CHOICES, unique=True, verbose_name="Year")

    def __str__(self):
        return self.get_name_display()

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

class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('Odd', 'Odd'),
        ('Even', 'Even'),
    ]
    semester_number = models.IntegerField(verbose_name="Semester Number",)
    session_year = models.ForeignKey(SessionYear, on_delete=models.CASCADE, related_name='semesters', verbose_name="Session Year")
    semester_type = models.CharField(max_length=10, choices=SEMESTER_CHOICES, verbose_name="Semester Type")

    class Meta:
        unique_together = ('session_year', 'semester_number')
        indexes = [
            models.Index(fields=['semester_number']),
            models.Index(fields=['semester_type']),
        ]

    def __str__(self):
        return f"{self.get_semester_type_display()} Semester {self.semester_number} - {self.session_year.academic_year} {self.session_year.department.name}"

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Course Code")
    name = models.CharField(max_length=100, verbose_name="Course Name")
    # department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses', verbose_name="Department")
    # year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='courses', verbose_name="Year")
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses', verbose_name="Semester", blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name} - {self.sem}"

    class Meta:
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
        ]

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
        # constraints = [
        #     models.UniqueConstraint(fields=['department'], name='unique_hod_per_department'),
        # ]
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
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name="Department")
    roll_number = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name="Roll Number")
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name="Semester")
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name="Year")
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, verbose_name="CGPA")
    mobile_no = models.CharField(max_length=15, blank=True, null=True, verbose_name="Mobile Number")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    courses = models.ManyToManyField(Course, related_name='students', blank=True, verbose_name="Courses")
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

class Lecture(models.Model):
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
        ]

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances', verbose_name="Course")
    lab_batch = models.ForeignKey(LabsBatches, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lab Batch")
    date = models.DateField(verbose_name="Date")
    present = models.BooleanField(default=False, verbose_name="Present")

    def __str__(self):
        return f"Attendance: {self.student.user.username} - {self.course.name} - {self.date} - {'Present' if self.present else 'Absent'}"

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['present']),
        ]

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



# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.Model):
#     USER_TYPE_CHOICES = [
#         ('STUDENT', 'Student'),
#         ('TEACHER', 'Teacher'),
#         ('STAFF', 'Staff'),
#         ('HOD', 'HOD'),
#         ('PRINCIPAL', 'Principal'),
#     ]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='STUDENT')

#     def __str__(self):
#         return f"{self.user.username} - {self.get_user_type_display()}"

# class Department(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     # year = models.ForeignKey('Year', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

# class Year(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name

# class Course(models.Model):
#     code = models.CharField(max_length=10, unique=True)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.code} - {self.name}"
    
# # class Course(models.Model):
# #     name = models.CharField(max_length=100)
# #     department = models.ForeignKey(Department, on_delete=models.CASCADE)
# #     year = models.ForeignKey('Year', on_delete=models.CASCADE)
    
# #     def __str__(self):
# #         return self.name
    

# class Program(models.Model):
#     name = models.CharField(max_length=100)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
#     year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='programs')
#     # semester = models.CharField(max_length=10)

#     def __str__(self):
#         return f"{self.name} - {self.department.name}"

# class Semester(models.Model):
#     SEMESTER_CHOICES = [
#         ('Odd', 'Odd'),
#         ('Even', 'Even'),
#     ]
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='semesters')
#     semester_type = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
#     semester_number = models.IntegerField(default=1)

#     class Meta:
#         unique_together = ('department', 'semester_number')

#     def __str__(self):
#         return f"{self.get_semester_type_display()} Semester {self.semester_number} - {self.department.name}"

# class HonorsMinors(models.Model):
#     name = models.CharField(max_length=100)
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='honors_minors', null=True, blank=True)

#     def __str__(self):
#         return self.name

# class LabsBatches(models.Model):
#     name = models.CharField(max_length=100)
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='labs_batches')
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='labs_batches')

#     def __str__(self):
#         return f"Lab Batch {self.name} - Program {self.program.name}"

# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
#     courses_taught = models.ManyToManyField(Course, blank=True, related_name='teachers')
#     faculty_id = models.CharField(max_length=10, unique=True)
#     mobile_no = models.CharField(max_length=15, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     experience = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"Teacher: {self.user.username} - Department: {self.department.name if self.department else 'No Department'}"
    
# # class Teacher(models.Model):
# #     name = models.CharField(max_length=100)
# #     username = models.CharField(max_length=100, unique=True)
# #     password = models.CharField(max_length=100)
# #     department = models.ForeignKey(Department, on_delete=models.CASCADE)
# #     courses = models.ManyToManyField('Course', related_name='teachers', blank=True)
# #     honors_minors = models.ForeignKey('HonorsMinors', on_delete=models.SET_NULL, null=True, blank=True)

# #     def __str__(self):
# #         return self.name



# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
#     roll_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
#     semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
#     year = models.CharField(max_length=20, null=True, blank=True)  # Allow character field for year
#     cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
#     mobile_no = models.CharField(max_length=15, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     courses = models.ManyToManyField('Course', related_name='students', blank=True)
#     lab_batch = models.ForeignKey(LabsBatches, on_delete=models.SET_NULL, null=True, blank=True)

#     def calculate_attendance_percentage(self):
#         total_classes = self.attendances.count()
#         attended_classes = self.attendances.filter(status='Present').count()
#         if total_classes > 0:
#             return (attended_classes / total_classes) * 100
#         return 0

#     def calculate_cgpa(self):
#         return self.cgpa

#     def __str__(self):
#         return f"Student: {self.user.username} - Roll No: {self.roll_number}"
    

# # class Student(models.Model):
# #     name = models.CharField(max_length=100)
# #     username = models.CharField(max_length=100, unique=True)
# #     password = models.CharField(max_length=100)
# #     department = models.ForeignKey(Department, on_delete=models.CASCADE)
# #     labs_batches = models.ForeignKey('LabsBatches', on_delete=models.SET_NULL, null=True, blank=True)
# #     odd_sem = models.ForeignKey('OddSem', on_delete=models.SET_NULL, null=True, blank=True)
# #     even_sem = models.ForeignKey('EvenSem', on_delete=models.SET_NULL, null=True, blank=True)
# #     honors_minors = models.ForeignKey('HonorsMinors', on_delete=models.SET_NULL, null=True, blank=True)
# #     year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True, blank=True)
# #     status = models.CharField(max_length=50, default='Active')
# #     attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
# #     cgpa_total = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Total CGPA
# #     courses = models.ManyToManyField('Course', related_name='students')

# #     def __str__(self):
# #         return self.name
    
# #     @property
# #     def attendance_percentage(self):
# #         total_lectures = Lecture.objects.filter(student=self).count()
# #         attended_lectures = Attendance.objects.filter(student=self, status='Present').count()
        
# #         if total_lectures > 0:
# #             return (attended_lectures / total_lectures) * 100
# #         return 0
    

# #     @property
# #     def cgpa_total(self):
# #         semester_cgpas = SemesterCGPA.objects.filter(student=self)
# #         total_cgpa = sum(cgpa.cgpa for cgpa in semester_cgpas)
# #         return total_cgpa
    
# #     @property
# #     def latest_cgpa(self):
# #         latest_cgpa_record = SemesterCGPA.objects.filter(student=self).order_by('-semester_number').first()
# #         if latest_cgpa_record:
# #             return latest_cgpa_record.cgpa
# #         return None



# class Enrollment(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments')

#     class Meta:
#         unique_together = ('student', 'course', 'semester')

#     def __str__(self):
#         return f"Enrollment: {self.student.user.username} in {self.course.name} - {self.semester}"


# from django.db import models
# from django.contrib.auth.models import User

# class HOD(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.OneToOneField('Department', on_delete=models.CASCADE, null=True, blank=True)  # Ensures only one HOD per department
#     office_number = models.CharField(max_length=20, blank=True, null=True)
#     managing_teachers = models.IntegerField()

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['department'], name='unique_hod_per_department')
#         ]

#     def __str__(self):
#         return f'{self.user.first_name} {self.user.last_name} - HOD of {self.department.name}'


# class Staff(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     position = models.CharField(max_length=100)
#     assigned_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
#     staff_id = models.CharField(max_length=10, unique=True)

#     def __str__(self):
#         return f"Staff: {self.user.username} - Position: {self.position}"

# from django.db import models
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError

# class Principal(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     office_location = models.CharField(max_length=255, default="Unknown Location")

#     class Meta:
#         permissions = [
#             ("can_view_principal", "Can view Principal details"),
#         ]

#     def __str__(self):
#         return f"Principal: {self.user.username} - Office: {self.office_location}"


# class Lecture(models.Model):
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='lectures')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='lectures')
#     date = models.DateField()

#     def __str__(self):
#         return f"Lecture on {self.date} for {self.course.name} - {self.program.name}"

# from django.db import models

# # Attendance Model with lab_batch, reason, and status fields
# class Attendance(models.Model):
#     STATUS_CHOICES = [
#         ('Present', 'Present'),
#         ('Absent', 'Absent'),
#         ('Sick Leave', 'Sick Leave'),
#         ('On Leave', 'On Leave'),
#         ('Permission Granted', 'Permission Granted'),
#     ]
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
#     lab_batch = models.ForeignKey(LabsBatches, on_delete=models.SET_NULL, null=True, blank=True)
#     date = models.DateField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Absent')
#     reason = models.TextField(blank=True, null=True)  # To capture reason for absence

#     def __str__(self):
#         return f"Attendance: {self.student.user.username} - {self.course.name} - {self.date}"


# # # Attendance Notification and Analysis
# # class AttendanceAnalysis:
# #     @staticmethod
# #     def notify_absentee(student, threshold=75):
# #         attendance_percentage = student.calculate_attendance_percentage()
# #         if attendance_percentage < threshold:
# #             subject = f"Low Attendance Alert for {student.user.username}"
# #             message = f"Dear {student.user.username}, your attendance is below {threshold}%. Please ensure regular attendance."
# #             recipient_list = [student.email]
# #             send_mail(subject, message, 'admin@institution.com', recipient_list)

# #     @staticmethod
# #     def generate_attendance_report(student):
# #         report = {
# #             'student': student.user.username,
# #             'attendance_percentage': student.calculate_attendance_percentage(),
# #             'cgpa': student.calculate_cgpa(),
# #         }
# #         return report


# class SemesterCGPA(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='semester_cgpas')
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='semester_cgpas')
#     cgpa = models.DecimalField(max_digits=4, decimal_places=2)

#     class Meta:
#         unique_together = ('student', 'semester')

#     def __str__(self):
#         return f"{self.student.user.username} - CGPA {self.cgpa} for Semester {self.semester.semester_number}"


# # models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.Model):
#     USER_TYPE_CHOICES = [
#         ('STUDENT', 'Student'),
#         ('TEACHER', 'Teacher'),
#         ('STAFF', 'Staff'),
#         ('HOD', 'HOD'),
#         ('PRINCIPAL', 'Principal'),
#     ]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

#     def __str__(self):
#         return f"{self.user.username} - {self.user_type}"

# class Department(models.Model):
#     name = models.CharField(max_length=100, default="Unknown Department")
#     year = models.ForeignKey('Year', on_delete=models.CASCADE, related_name='departments')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class Year(models.Model):
#     name = models.CharField(max_length=100, default="Unknown Year")

#     def __str__(self):
#         return self.name

# class Course(models.Model):
#     name = models.CharField(max_length=100, default="Unknown Course")
#     code = models.CharField(max_length=10, unique=True, default="UNKNOWN")

#     def __str__(self):
#         return self.name

# class Program(models.Model):
#     name = models.CharField(max_length=100, default="Unknown Program")
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='programs')
#     semester = models.CharField(max_length=10, default="Unknown Semester")

#     def __str__(self):
#         return f"{self.name} - {self.semester}"

# class EvenSem(models.Model):
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     program = models.ForeignKey('Program', on_delete=models.CASCADE)
#     semester_number = models.IntegerField(default=1)  # Add this field to track semester number

#     def __str__(self):
#         return f"Sem {self.semester_number} - Even {self.department.name}"


# class OddSem(models.Model):
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     program = models.ForeignKey('Program', on_delete=models.CASCADE)
#     semester_number = models.IntegerField(default=1)  # Add this field to track semester number

#     def __str__(self):
#         return f"Sem {self.semester_number} - Odd {self.department.name}"

# class HonorsMinors(models.Model):
#     name = models.CharField(max_length=100)
#     even_sem = models.ForeignKey('EvenSem', on_delete=models.CASCADE,null=True,blank=True)
#     odd_sem = models.ForeignKey('OddSem', on_delete=models.CASCADE,null=True,blank=True)

#     def __str__(self):
#         return self.name

# class LabsBatches(models.Model):
#     name = models.CharField(max_length=100, default="Unknown Lab Batch")
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='labs_batches')
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='labs_batches')

#     def __str__(self):
#         return f"Lab Batch {self.name} - Program {self.program.name if self.program else 'Unknown Program'}"

# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
#     # program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
#     courses_taught = models.ManyToManyField(Course, blank=True)
#     faculty_id = models.CharField(max_length=10, unique=True, default="UNKNOWN")
#     mobile_no = models.CharField(max_length=15, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     experience = models.TextField(blank=True, null=True)

#     class Meta:
#         permissions = [
#             ("can_view_student_data", "Can view student data"),
#         ]

#     def __str__(self):
#         return f"Teacher: {self.user.username} - Department: {self.department.name if self.department else 'No Department'}"

# # models.py

# from django.db import models
# from django.contrib.auth.models import User

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
#     roll_number = models.CharField(max_length=10, unique=True, null=True, blank=True, default=None)
#     # odd_sem = models.ForeignKey('OddSem', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
#     # even_sem = models.ForeignKey('EvenSem', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
#     year = models.IntegerField(blank=True,null=True)
#     cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
#     mobile_no = models.CharField(max_length=15, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     courses = models.ManyToManyField('Course', related_name='students', blank=True)  # Add this field


#     class Meta:
#         permissions = [
#             ("can_view_student", "Can view student details"),
#         ]

#     def __str__(self):
#         return f"Student: {self.user.username} - Roll No: {self.roll_number if self.roll_number else 'No Roll Number'}"

# class HOD(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='hods')
#     office_number = models.CharField(max_length=50, default="Unknown")
#     managing_teachers = models.IntegerField(default=0)

#     class Meta:
#         permissions = [
#             ("can_view_hod", "Can view HOD details"),
#         ]

#     def __str__(self):
#         return f"HOD: {self.user.username} - {self.department.name if self.department else 'No Department'}"

# class Staff(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     position = models.CharField(max_length=100, default="Unknown Position")
#     assigned_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
#     staff_id = models.CharField(max_length=10, unique=True, default="UNKNOWN")

#     class Meta:
#         permissions = [
#             ("can_view_staff", "Can view staff details"),
#         ]

#     def __str__(self):
#         return f"Staff: {self.user.username} - Position: {self.position}"

# class Principal(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     office_location = models.CharField(max_length=255, default="Unknown Location")
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='principals')

#     class Meta:
#         permissions = [
#             ("can_view_principal", "Can view Principal details"),
#         ]

#     def __str__(self):
#         return f"Principal: {self.user.username} - Department: {self.department.name if self.department else 'No Department'}"

# class Lecture(models.Model):
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='lectures')
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lectures')

#     def __str__(self):
#         return f"Lecture for {self.program.name if self.program else 'Unknown Program'} - Student {self.student.user.username if self.student else 'Unknown Student'}"

# class Attendance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(max_length=20)  # e.g., "Present", "Absent", etc.
#     is_present = models.BooleanField(default=False)  # Add this if needed

#     def __str__(self):
#         return f"{self.student.username} - {self.lecture.program.name} - {self.date} - {self.status}"


# class SemesterCGPA(models.Model):
#     SEMESTER_CHOICES = [
#         ('Odd', 'Odd'),
#         ('Even', 'Even'),
#     ]
    
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     semester_type = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
#     semester_number = models.PositiveIntegerField()  # e.g., 1, 2, 3, etc.
#     cgpa = models.DecimalField(max_digits=4, decimal_places=2)

#     def __str__(self):
#         return f"{self.student.name} - {self.get_semester_type_display()} Semester {self.semester_number} CGPA: {self.cgpa}"
    
#     # class Student(models.Model):
#     # name = models.CharField(max_length=100)
#     # username = models.CharField(max_length=100, unique=True)
#     # password = models.CharField(max_length=100)
#     # department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     # labs_batches = models.ForeignKey('LabsBatches', on_delete=models.SET_NULL, null=True, blank=True)
#     # odd_sem = models.ForeignKey('OddSem', on_delete=models.SET_NULL, null=True, blank=True)
#     # even_sem = models.ForeignKey('EvenSem', on_delete=models.SET_NULL, null=True, blank=True)
#     # honors_minors = models.ForeignKey('HonorsMinors', on_delete=models.SET_NULL, null=True, blank=True)
#     # year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True, blank=True)
#     # status = models.CharField(max_length=50, default='Active')
#     # attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     # cgpa_total = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Total CGPA

#     # def __str__(self):
#     #     return self.name
    
#     # @property
#     # def attendance_percentage(self):
#     #     total_lectures = Lecture.objects.filter(student=self).count()
#     #     attended_lectures = Attendance.objects.filter(student=self, status='Present').count()
        
#     #     if total_lectures > 0:
#     #         return (attended_lectures / total_lectures) * 100
#     #     return 0
    

#     # @property
#     # def cgpa_total(self):
#     #     semester_cgpas = SemesterCGPA.objects.filter(student=self)
#     #     total_cgpa = sum(cgpa.cgpa for cgpa in semester_cgpas)
#     #     return total_cgpa
    
#     # @property
#     # def latest_cgpa(self):
#     #     latest_cgpa_record = SemesterCGPA.objects.filter(student=self).order_by('-semester_number').first()
#     #     if latest_cgpa_record:
#     #         return latest_cgpa_record.cgpa
#     #     return None



