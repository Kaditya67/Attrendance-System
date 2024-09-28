from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from myapp.models import Principal, Department
import csv

class Command(BaseCommand):
    help = 'Import Principal details from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import Principal data from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)

                # Check if a Principal already exists
                existing_principal = Principal.objects.first()

                if existing_principal:
                    self.stdout.write(self.style.WARNING(f"A principal already exists: {existing_principal.user.username}. Updating principal data."))
                
                for row in reader:
                    # Get or create user
                    user, created = User.objects.get_or_create(
                        username=row['username'],
                        defaults={
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                        }
                    )

                    # Create or update Principal
                    principal, created = Principal.objects.update_or_create(
                        user=user,
                        defaults={
                            'office_location': row['office_location']
                        }
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully added/updated Principal {user.username}'))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
