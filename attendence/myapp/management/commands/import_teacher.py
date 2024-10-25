from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from myapp.models import Teacher, Department, Course
import csv

class Command(BaseCommand):
    help = 'Import Teacher details from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import Teacher data from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            # Ensure the Teacher group exists
            teacher_group, created = Group.objects.get_or_create(name='Teacher')
            if created:
                self.stdout.write(self.style.SUCCESS('Teacher group created.'))

            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Validate required fields
                    required_fields = ['username', 'first_name', 'last_name', 'faculty_id', 'assigned_department']
                    missing_fields = [field for field in required_fields if not row.get(field)]

                    if missing_fields:
                        self.stdout.write(self.style.ERROR(f"Missing fields {', '.join(missing_fields)} for row: {row}"))
                        continue

                    # Extract and clean up email
                    email = row.get('email', '').strip()

                    # Validate email
                    if email and not self.is_valid_email(email):
                        self.stdout.write(self.style.ERROR(f"Invalid email '{email}' for username {row['username']}"))
                        continue

                    # Get or create department
                    department_name = row['assigned_department'].strip()
                    department = Department.objects.filter(name=department_name).first()

                    if not department:
                        self.stdout.write(self.style.ERROR(f"Department '{department_name}' not found for username {row['username']}"))
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

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'User {user.username} created.'))

                    # Add user to the Teacher group
                    if not user.groups.filter(name='Teacher').exists():
                        user.groups.add(teacher_group)
                        self.stdout.write(self.style.SUCCESS(f'User {user.username} added to Teacher group.'))

                    # Create or update Teacher details
                    teacher, created = Teacher.objects.update_or_create(
                        user=user,
                        defaults={
                            'faculty_id': row['faculty_id'],
                            'department': department,
                            'mobile_no': row.get('mobile_no', '').strip(),
                            'email': email,
                            'experience': row.get('experience', '').strip(),
                        }
                    )

                    # Handle courses_taught
                    courses_taught_codes = row.get('courses_taught', '').split(',')
                    for code in [c.strip() for c in courses_taught_codes if c.strip()]:
                        course, created = Course.objects.get_or_create(code=code, defaults={'name': code})
                        teacher.courses_taught.add(course)

                    # Handle assigned_courses
                    assigned_courses_codes = row.get('assigned_courses', '').split(',')
                    for code in [c.strip() for c in assigned_courses_codes if c.strip()]:
                        course, created = Course.objects.get_or_create(code=code, defaults={'name': code})
                        teacher.assigned_courses.add(course)

                    teacher.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully added/updated Teacher {user.username}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")

    def is_valid_email(self, email):
        """Basic email validation to check if it ends with '@dbit.in'."""
        return email.endswith('@dbit.in')
