from django.core.management.base import BaseCommand, CommandError
from myapp.models import LabsBatches, Program, Department
import csv

class Command(BaseCommand):
    help = 'Import lab batches from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to import lab batches from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Validate required fields
                    required_fields = ['name', 'program', 'department']
                    missing_fields = [field for field in required_fields if not row.get(field)]
                    
                    if missing_fields:
                        self.stdout.write(self.style.ERROR(f"Missing fields {', '.join(missing_fields)} for row: {row}"))
                        continue

                    # Get or create program
                    program_name = row['program'].strip()
                    program, created = Program.objects.get_or_create(name=program_name)

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created new program '{program_name}'"))

                    # Get or create department
                    department_name = row['department'].strip()
                    department = Department.objects.filter(name=department_name).first()

                    if not department:
                        self.stdout.write(self.style.ERROR(f"Department '{department_name}' not found for lab batch '{row['name']}'"))
                        continue

                    # Create lab batch
                    lab_batch, created = LabsBatches.objects.get_or_create(
                        name=row['name'].strip(),
                        defaults={'program': program, 'department': department}
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created new lab batch '{lab_batch.name}'"))

        except FileNotFoundError:
            raise CommandError(f"File '{csv_file}' does not exist")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
