from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from myapp.models import Student, Department, Year
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
                    required_fields = ['username', 'first_name', 'last_name', 'email', 'department', 'roll_number', 'year_of_study']
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

                    # Get or create year
                    year_name = row['year_of_study'].strip()
                    if not year_name.isdigit():
                        self.stdout.write(self.style.ERROR(f"Invalid year_of_study '{year_name}' for username {row['username']}"))
                        continue
                    year, created = Year.objects.get_or_create(name=year_name)

                    # Create or update student details
                    student, created = Student.objects.update_or_create(
                        user=user,
                        defaults={
                            'department': department,
                            'roll_number': row['roll_number'].strip(),
                            'year': year,
                            'mobile_no': row.get('mobile_no', '').strip(),
                            'address': row.get('address', '').strip(),
                            'email': email,  # Ensure this field is set
                        }
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully added/updated student {user.username}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")

    def is_valid_email(self, email):
        """Basic email validation to check if it ends with '@dbit.in'."""
        return email.endswith('@dbit.in') and '@' in email
