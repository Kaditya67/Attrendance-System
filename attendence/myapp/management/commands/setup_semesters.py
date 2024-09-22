# myapp/management/commands/setup_semesters.py

from django.core.management.base import BaseCommand
from myapp.models import Semester, SessionYear, Year

class Command(BaseCommand):
    help = 'Set up semesters for each department and session year'

    def handle(self, *args, **kwargs):
        year_choices = ['FE', 'SE', 'TE', 'BE']
        
        for department in SessionYear.objects.all():
            session_year = department
            for i, year_name in enumerate(year_choices):
                for semester_number in range(1, 3):  # 1 for Odd, 2 for Even
                    semester_type = 'Odd' if semester_number == 1 else 'Even'
                    semester_num = (i * 2) + semester_number  # Calculate the unique semester number

                    # Create or get semester
                    semester, created = Semester.objects.get_or_create(
                        semester_number=semester_num,
                        session_year=session_year,
                        semester_type=semester_type,
                        year=Year.objects.get(name=year_name),
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added: {semester}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'Semester already exists: {semester}'))
