from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from myapp.models import Staff, Department
import csv

class Command(BaseCommand):
    help = 'Import Staff details from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import Staff data from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Validate required fields
                    required_fields = ['username', 'first_name', 'last_name', 'position', 'assigned_department', 'staff_id']
                    missing_fields = [field for field in required_fields if not row.get(field)]

                    if missing_fields:
                        self.stdout.write(self.style.ERROR(f"Missing fields {', '.join(missing_fields)} for row: {row}"))
                        continue

                    # Extract and clean up department
                    department_name = row['assigned_department'].strip()
                    department = Department.objects.filter(name=department_name).first()

                    if not department:
                        self.stdout.write(self.style.ERROR(f"Department '{department_name}' not found for username {row['username']}"))
                        continue

                    # Get or create user
                    user, created = User.objects.get_or_create(
                        username=row['username'],
                        defaults={
                            'first_name': row['first_name'].strip(),
                            'last_name': row['last_name'].strip(),
                        }
                    )

                    # Create or update Staff details
                    try:
                        staff, created = Staff.objects.update_or_create(
                            user=user,
                            defaults={
                                'position': row['position'].strip(),
                                'assigned_department': department,
                                'staff_id': row['staff_id'].strip()
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f'Successfully added/updated Staff {user.username}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error updating/creating Staff {user.username}: {str(e)}"))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
