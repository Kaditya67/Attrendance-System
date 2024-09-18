from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from myapp.models import HOD, Department
import csv

class Command(BaseCommand):
    help = 'Import HOD details from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import HOD data from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Extract department
                    department = Department.objects.filter(name=row['department']).first()

                    # Get or create user
                    user, created = User.objects.get_or_create(
                        username=row['username'],
                        defaults={
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                        }
                    )

                    # Create or update HOD details
                    hod, created = HOD.objects.update_or_create(
                        user=user,
                        defaults={
                            'department': department,
                            'office_number': row['office_number'],
                            'managing_teachers': row['managing_teachers']
                        }
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully added/updated HOD {user.username}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
