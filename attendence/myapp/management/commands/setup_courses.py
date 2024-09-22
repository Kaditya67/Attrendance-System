# myapp/management/commands/setup_courses.py

from django.core.management.base import BaseCommand
from myapp.models import Course, Semester

class Command(BaseCommand):
    help = 'Set up courses for each semester'

    def handle(self, *args, **kwargs):
        # Example course data
        course_data = [
            {"code": "CS101", "name": "Introduction to Computer Science", "sem": 1},
            {"code": "CS102", "name": "Data Structures", "sem": 2},
            {"code": "ME101", "name": "Engineering Mechanics", "sem": 1},
            {"code": "IT101", "name": "Information Technology Fundamentals", "sem": 1},
            # Add more courses as needed
        ]

        for data in course_data:
            try:
                semester = Semester.objects.get(semester_number=data["sem"])  # Adjust the query based on your logic
                course, created = Course.objects.get_or_create(
                    code=data["code"],
                    name=data["name"],
                    sem=semester
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully added Course: {course}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Course already exists: {course}'))
            except Semester.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Semester with number {data["sem"]} does not exist.'))
