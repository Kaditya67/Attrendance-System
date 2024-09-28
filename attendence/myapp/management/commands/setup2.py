from django.core.management.base import BaseCommand
from myapp.models import SessionYear, Semester

class Command(BaseCommand):
    help = 'Populate semesters for each department'

    def handle(self, *args, **kwargs):
        # Define the semester details with corresponding year designations
        semester_details = [
            (1, 'Odd', 'FE'),
            (2, 'Even', 'FE'),
            (3, 'Odd', 'SE'),
            (4, 'Even', 'SE'),
            (5, 'Odd', 'TE'),
            (6, 'Even', 'TE'),
            (7, 'Odd', 'BE'),
            (8, 'Even', 'BE'),
        ]

        # Get all session years
        session_years = SessionYear.objects.all()

        for session_year in session_years:
            for semester_number, semester_type, year in semester_details:
                try:
                    semester = Semester.objects.create(
                        semester_number=semester_number,
                        session_year=session_year,
                        semester_type=semester_type,
                        year=year  # Directly use the specified year
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully added: {semester}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding semester: {e}'))
