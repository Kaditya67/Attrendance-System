from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from myapp.models import Student, Department
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
                    # Extract and clean up email
                    email = row.get('email', '').strip()  # Strip any whitespace

                    # Debug: Print email to check if it's being extracted
                    print(f"Extracted email: {email} for username: {row['username']}")

                    if not email:
                        self.stdout.write(self.style.ERROR(f"Missing email for user {row['username']}"))
                        continue  # Skip this row if email is missing

                    # Get or create user
                    user, created = User.objects.get_or_create(
                        username=row['username'],
                        defaults={
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                        }
                    )

                    # Debug: Print to check if user is created or found
                    print(f"User {user.username} {'created' if created else 'found'}")

                    # If user is not newly created, check and update email
                    if user.email != email:
                        user.email = email
                        user.save()  # Save the updated email to the database

                        # Debug: Check if email was saved properly
                        print(f"Updated email for user {user.username} to {user.email}")
                    else:
                        # Debug: If email was already correct
                        print(f"Email for user {user.username} already up to date: {user.email}")

                    # Get department (if exists)
                    department = Department.objects.filter(name=row['department']).first()

                    # Create or update student details
                    student, created = Student.objects.update_or_create(
                        user=user,
                        defaults={
                            'department': department,
                            'roll_number': row['roll_number'],
                            'year': row['year'],
                            'cgpa': row['cgpa'],
                            'mobile_no': row['mobile_no'],
                            'address': row['address']
                        }
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully added/updated student {user.username}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
