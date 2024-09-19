from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from myapp.models import Student, Department, Semester, Course, LabsBatches, Program
import csv

class Command(BaseCommand):
    help = 'Import student details from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import student data from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Validate required fields
                    required_fields = ['username', 'first_name', 'last_name', 'email', 'department', 'roll_number', 'semester_type', 'semester_number', 'year', 'cgpa', 'mobile_no', 'address', 'courses', 'lab_batch', 'program']
                    missing_fields = [field for field in required_fields if not row.get(field)]
                    
                    if missing_fields:
                        self.stdout.write(self.style.ERROR(f"Missing fields {', '.join(missing_fields)} for row: {row}"))
                        continue

                    # Extract and clean up email
                    email = row['email'].strip()

                    # Validate email
                    if not email or not self.is_valid_email(email):
                        self.stdout.write(self.style.ERROR(f"Invalid email '{email}' for username {row['username']}"))
                        continue

                    # Get or create user
                    user, created = User.objects.get_or_create(
                        username=row['username'],
                        defaults={
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                            'email': email,
                        }
                    )

                    # Update email if user exists and email is different
                    if not created and user.email != email:
                        user.email = email
                        user.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated email for user {user.username}"))

                    # Get or create department
                    department_name = row['department'].strip()
                    department = Department.objects.filter(name=department_name).first()

                    if not department:
                        self.stdout.write(self.style.ERROR(f"Department '{department_name}' not found for username {row['username']}"))
                        continue

                    # Get or create program
                    program_name = row.get('program', '').strip()
                    program, created = Program.objects.get_or_create(name=program_name)

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created new program '{program_name}'"))

                    # Get or create semester
                    semester_type = row['semester_type'].strip()
                    semester_number = int(row['semester_number'].strip())
                    semester, created = Semester.objects.get_or_create(
                        department=department,
                        semester_type=semester_type,
                        semester_number=semester_number
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created new semester '{semester_type} {semester_number}'"))

                    # Get or create course
                    course_name = row['courses'].strip()
                    course, created = Course.objects.get_or_create(
                        code=course_name,  # Use code for uniqueness
                        defaults={'name': course_name}
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created new course '{course_name}'"))

                    # Get or create lab_batch
                    lab_batch_name = row['lab_batch'].strip()
                    # Create or update lab batch with department and program
                    lab_batch, created = LabsBatches.objects.get_or_create(
                        name=lab_batch_name,
                        defaults={'department': department, 'program': program}
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created new lab batch '{lab_batch_name}' for department '{department_name}' and program '{program_name}'"))

                    # Create or update student details
                    student, created = Student.objects.update_or_create(
                        user=user,
                        defaults={
                            'department': department,
                            'roll_number': row['roll_number'].strip(),
                            'semester': semester,
                            'year': row['year'].strip(),
                            'cgpa': float(row['cgpa'].strip()),
                            'mobile_no': row.get('mobile_no', '').strip(),
                            'address': row.get('address', '').strip(),
                            'email': email,  # Ensure this field is set
                            'lab_batch': lab_batch,
                        }
                    )

                    # Add courses to student
                    student.courses.add(course)

                    self.stdout.write(self.style.SUCCESS(f'Successfully added/updated student {user.username}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")

    def is_valid_email(self, email):
        """Basic email validation to check if it ends with '@dbit.in'."""
        return email.endswith('@dbit.in') and '@' in email
