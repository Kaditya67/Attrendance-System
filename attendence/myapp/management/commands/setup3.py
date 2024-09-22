from django.core.management.base import BaseCommand
from myapp.models import Course, Semester

class Command(BaseCommand):
    help = 'Setup courses for each semester'

    def handle(self, *args, **kwargs):
        courses_data = [
            # Electronics and Telecommunication
            # First Year
            ('ET101', 'Circuit Theory', 1, 1),  # Odd Semester 1
            ('ET102', 'Digital Electronics', 1, 1),
            ('ET103', 'Network Theory', 1, 1),
            ('ET104', 'Microcontrollers', 1, 1),
            ('ET105', 'Electronics Lab', 1, 1),
            ('ET201', 'Signals and Systems', 1, 2),  # Even Semester 2
            ('ET202', 'Control Systems', 1, 2),
            ('ET203', 'Communication Systems', 1, 2),
            ('ET204', 'Microprocessors', 1, 2),
            ('ET205', 'Telecommunication Lab', 1, 2),
            # Second Year
            ('ET301', 'Advanced Circuit Design', 1, 3),  # Odd Semester 3
            ('ET302', 'Embedded Systems', 1, 3),
            ('ET303', 'VLSI Design', 1, 3),
            ('ET304', 'Signal Processing', 1, 3),
            ('ET305', 'Digital Signal Processing Lab', 1, 3),
            ('ET401', 'Wireless Communication', 1, 4),  # Even Semester 4
            ('ET402', 'Optical Communication', 1, 4),
            ('ET403', 'Control Theory', 1, 4),
            ('ET404', 'Robotics', 1, 4),
            ('ET405', 'Communication Lab', 1, 4),
            # Third Year
            ('ET501', 'Radar Systems', 1, 5),  # Odd Semester 5
            ('ET502', 'Advanced Embedded Systems', 1, 5),
            ('ET503', 'Telematics', 1, 5),
            ('ET504', 'Internet of Things', 1, 5),
            ('ET505', 'Project Work', 1, 5),
            ('ET601', 'Advanced Networking', 1, 6),  # Even Semester 6
            ('ET602', 'Machine Learning', 1, 6),
            ('ET603', 'Smart Sensors', 1, 6),
            ('ET604', 'Artificial Intelligence', 1, 6),
            ('ET605', 'Research Project', 1, 6),
            # Fourth Year
            ('ET701', 'Project Management', 1, 7),  # Odd Semester 7
            ('ET702', 'Industry Internship', 1, 7),
            ('ET703', 'Entrepreneurship', 1, 7),
            ('ET704', 'Capstone Project', 1, 7),
            ('ET705', 'Thesis', 1, 7),
            ('ET801', 'Elective Course 1', 1, 8),  # Even Semester 8
            ('ET802', 'Elective Course 2', 1, 8),
            ('ET803', 'Elective Course 3', 1, 8),
            ('ET804', 'Elective Course 4', 1, 8),
            ('ET805', 'Elective Course 5', 1, 8),

            # Computer Science
            # First Year
            ('CS101', 'Introduction to Computer Science', 1, 1),  # Odd Semester 1
            ('CS102', 'Data Structures', 1, 1),
            ('CS103', 'Discrete Mathematics', 1, 1),
            ('CS104', 'Computer Organization', 1, 1),
            ('CS105', 'CS Lab', 1, 1),
            ('CS201', 'Algorithms', 1, 2),  # Even Semester 2
            ('CS202', 'Operating Systems', 1, 2),
            ('CS203', 'Database Systems', 1, 2),
            ('CS204', 'Software Engineering', 1, 2),
            ('CS205', 'DBMS Lab', 1, 2),
            # Second Year
            ('CS301', 'Web Development', 1, 3),  # Odd Semester 3
            ('CS302', 'Software Architecture', 1, 3),
            ('CS303', 'Computer Networks', 1, 3),
            ('CS304', 'Human-Computer Interaction', 1, 3),
            ('CS305', 'Web Lab', 1, 3),
            ('CS401', 'Mobile Application Development', 1, 4),  # Even Semester 4
            ('CS402', 'Cloud Computing', 1, 4),
            ('CS403', 'Cyber Security', 1, 4),
            ('CS404', 'Game Development', 1, 4),
            ('CS405', 'Security Lab', 1, 4),
            # Third Year
            ('CS501', 'Data Mining', 1, 5),  # Odd Semester 5
            ('CS502', 'Machine Learning', 1, 5),
            ('CS503', 'Big Data Analytics', 1, 5),
            ('CS504', 'Blockchain Technology', 1, 5),
            ('CS505', 'Project Work', 1, 5),
            ('CS601', 'Advanced Databases', 1, 6),  # Even Semester 6
            ('CS602', 'Natural Language Processing', 1, 6),
            ('CS603', 'Artificial Intelligence', 1, 6),
            ('CS604', 'Computer Vision', 1, 6),
            ('CS605', 'Research Project', 1, 6),
            # Fourth Year
            ('CS701', 'Capstone Project', 1, 7),  # Odd Semester 7
            ('CS702', 'Industry Internship', 1, 7),
            ('CS703', 'Entrepreneurship', 1, 7),
            ('CS704', 'Thesis', 1, 7),
            ('CS705', 'Elective Course 1', 1, 7),
            ('CS801', 'Elective Course 2', 1, 8),  # Even Semester 8
            ('CS802', 'Elective Course 3', 1, 8),
            ('CS803', 'Elective Course 4', 1, 8),
            ('CS804', 'Elective Course 5', 1, 8),
            ('CS805', 'Elective Course 6', 1, 8),

            # Information Technology
            # First Year
            ('IT101', 'Web Technologies', 1, 1),  # Odd Semester 1
            ('IT102', 'Network Fundamentals', 1, 1),
            ('IT103', 'System Analysis', 1, 1),
            ('IT104', 'Programming Fundamentals', 1, 1),
            ('IT105', 'IT Lab', 1, 1),
            ('IT201', 'Computer Networks', 1, 2),  # Even Semester 2
            ('IT202', 'Mobile Computing', 1, 2),
            ('IT203', 'Software Testing', 1, 2),
            ('IT204', 'Project Management', 1, 2),
            ('IT205', 'Networking Lab', 1, 2),
            # Second Year
            ('IT301', 'Information Security', 1, 3),  # Odd Semester 3
            ('IT302', 'Web Application Development', 1, 3),
            ('IT303', 'Data Analytics', 1, 3),
            ('IT304', 'UI/UX Design', 1, 3),
            ('IT305', 'Web Lab', 1, 3),
            ('IT401', 'Cloud Computing', 1, 4),  # Even Semester 4
            ('IT402', 'Mobile Application Development', 1, 4),
            ('IT403', 'E-Commerce', 1, 4),
            ('IT404', 'DevOps', 1, 4),
            ('IT405', 'Cloud Lab', 1, 4),
            # Third Year
            ('IT501', 'Data Warehousing', 1, 5),  # Odd Semester 5
            ('IT502', 'Artificial Intelligence', 1, 5),
            ('IT503', 'Big Data', 1, 5),
            ('IT504', 'Data Visualization', 1, 5),
            ('IT505', 'Project Work', 1, 5),
            ('IT601', 'Machine Learning', 1, 6),  # Even Semester 6
            ('IT602', 'IoT Systems', 1, 6),
            ('IT603', 'Advanced Networking', 1, 6),
            ('IT604', 'Information Retrieval', 1, 6),
            ('IT605', 'Research Project', 1, 6),
            # Fourth Year
            ('IT701', 'Capstone Project', 1, 7),  # Odd Semester 7
            ('IT702', 'Industry Internship', 1, 7),
            ('IT703', 'Entrepreneurship', 1, 7),
            ('IT704', 'Thesis', 1, 7),
            ('IT705', 'Elective Course 1', 1, 7),
            ('IT801', 'Elective Course 2', 1, 8),  # Even Semester 8
            ('IT802', 'Elective Course 3', 1, 8),
            ('IT803', 'Elective Course 4', 1, 8),
            ('IT804', 'Elective Course 5', 1, 8),
            ('IT805', 'Elective Course 6', 1, 8),

            # Mechanical Engineering
            # First Year
            ('ME101', 'Engineering Mechanics', 1, 1),  # Odd Semester 1
            ('ME102', 'Thermodynamics', 1, 1),
            ('ME103', 'Fluid Mechanics', 1, 1),
            ('ME104', 'Material Science', 1, 1),
            ('ME105', 'Mechanical Lab', 1, 1),
            ('ME201', 'Machine Design', 1, 2),  # Even Semester 2
            ('ME202', 'Manufacturing Processes', 1, 2),
            ('ME203', 'Heat Transfer', 1, 2),
            ('ME204', 'Production Engineering', 1, 2),
            ('ME205', 'Manufacturing Lab', 1, 2),
            # Second Year
            ('ME301', 'Mechanics of Materials', 1, 3),  # Odd Semester 3
            ('ME302', 'Kinematics', 1, 3),
            ('ME303', 'Thermal Engineering', 1, 3),
            ('ME304', 'Fluid Machinery', 1, 3),
            ('ME305', 'Lab Work', 1, 3),
            ('ME401', 'Automobile Engineering', 1, 4),  # Even Semester 4
            ('ME402', 'Robotics', 1, 4),
            ('ME403', 'Computer-Aided Design', 1, 4),
            ('ME404', 'Production Management', 1, 4),
            ('ME405', 'Robotics Lab', 1, 4),
            # Third Year
            ('ME501', 'Design of Machine Elements', 1, 5),  # Odd Semester 5
            ('ME502', 'Engineering Dynamics', 1, 5),
            ('ME503', 'Advanced Manufacturing', 1, 5),
            ('ME504', 'Thermal System Design', 1, 5),
            ('ME505', 'Project Work', 1, 5),
            ('ME601', 'Advanced Materials', 1, 6),  # Even Semester 6
            ('ME602', 'Energy Systems', 1, 6),
            ('ME603', 'Automation', 1, 6),
            ('ME604', 'Renewable Energy', 1, 6),
            ('ME605', 'Research Project', 1, 6),
            # Fourth Year
            ('ME701', 'Capstone Project', 1, 7),  # Odd Semester 7
            ('ME702', 'Industry Internship', 1, 7),
            ('ME703', 'Entrepreneurship', 1, 7),
            ('ME704', 'Thesis', 1, 7),
            ('ME705', 'Elective Course 1', 1, 7),
            ('ME801', 'Elective Course 2', 1, 8),  # Even Semester 8
            ('ME802', 'Elective Course 3', 1, 8),
            ('ME803', 'Elective Course 4', 1, 8),
            ('ME804', 'Elective Course 5', 1, 8),
            ('ME805', 'Elective Course 6', 1, 8),
        ]

        for code, name, session_year_id, semester_number in courses_data:
            try:
                semester = Semester.objects.get(session_year_id=session_year_id, semester_number=semester_number)
                course = Course(code=code, name=name, sem=semester)
                course.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added course: {course}'))
            except Semester.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Semester does not exist for session year {session_year_id} and semester number {semester_number}.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding course: {e}'))
