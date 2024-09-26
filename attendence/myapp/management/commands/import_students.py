from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import transaction
from myapp.models import Student, Semester
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
                students_to_create = []

                with transaction.atomic():
                    for row in reader:
                        # Validate required fields
                        required_fields = ['username', 'first_name', 'last_name', 'email', 'roll_number', 'semester', 'mobile_no', 'address', 'student_id']
                        missing_fields = [field for field in required_fields if not row.get(field)]

                        if missing_fields:
                            self.stdout.write(self.style.ERROR(f"Missing fields {', '.join(missing_fields)} for row: {row}"))
                            continue

                        # Extract and clean up email
                        email = row['email'].strip()

                        # Validate email
                        if not self.is_valid_email(email):
                            self.stdout.write(self.style.ERROR(f"Invalid email '{email}' for username {row['username']}"))
                            continue

                        # Validate and fetch semester
                        try:
                            semester = Semester.objects.get(pk=row['semester'].strip())
                        except Semester.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f"Semester ID '{row['semester']}' does not exist for student {row['username']}"))
                            continue

                        # Get or create user
                        user, created = User.objects.get_or_create(
                            username=row['username'].strip(),
                            defaults={
                                'first_name': row['first_name'].strip(),
                                'last_name': row['last_name'].strip(),
                                'email': email,
                            }
                        )

                        if not created:
                            # Update user if it already exists
                            user.first_name = row['first_name'].strip()
                            user.last_name = row['last_name'].strip()
                            user.email = email
                            user.save()

                        # Prepare student data for creation or update
                        student_data = {
                            'student_id': row['student_id'].strip(),
                            'roll_number': row['roll_number'].strip(),
                            'semester': semester,
                            'mobile_no': row['mobile_no'].strip() if row.get('mobile_no') else None,
                            'address': row['address'].strip() if row.get('address') else None,
                            'email': email,
                        }

                        # Create or update student
                        student, created = Student.objects.update_or_create(
                            user=user,
                            defaults=student_data
                        )

                        students_to_create.append(student)

                        self.stdout.write(self.style.SUCCESS(f"Successfully added/updated student {user.username}"))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist.")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")

    def is_valid_email(self, email):
        """Basic email validation to check if it ends with '@dbit.in'."""
        return email.endswith('@dbit.in') and '@' in email
