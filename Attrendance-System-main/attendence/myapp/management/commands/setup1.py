# myapp/management/commands/setup_initial_data.py

from django.core.management.base import BaseCommand
from myapp.models import Department, Year, SessionYear

class Command(BaseCommand):
    help = 'Set up initial data for the application without semesters'

    def handle(self, *args, **kwargs):
        # Step 1: Add Departments
        departments_data = [
            "Information Technology",
            "Computer Science",
            "Mechanical",
            "Electronics and Telecommunication"
        ]

        for dept_name in departments_data:
            department, created = Department.objects.get_or_create(name=dept_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added Department: {department.name}'))

        # Step 2: Add Years
        year_choices = ['FE', 'SE', 'TE', 'BE']
        for year_name in year_choices:
            year, created = Year.objects.get_or_create(name=year_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added Year: {year.name}'))

        # Step 3: Add Session Years
        session_year_data = '2023-2024'
        for department in Department.objects.all():
            session_year, created = SessionYear.objects.get_or_create(
                academic_year=session_year_data,
                department=department,
                defaults={'start_date': '2023-08-01', 'end_date': '2024-05-31'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added Session Year: {session_year}'))
            else:
                self.stdout.write(self.style.WARNING(f'Session Year already exists: {session_year}'))
