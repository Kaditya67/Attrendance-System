from django.core.management.base import BaseCommand
from myapp.models import Course

class Command(BaseCommand):
    help = 'Setup courses for each semester'

    def handle(self, *args, **kwargs):
        courses_data = [
            # Electronics and Telecommunication
            # First Year
            ('ET101', 'Circuit Theory'),
            ('ET102', 'Digital Electronics'),
            ('ET103', 'Network Theory'),
            ('ET104', 'Microcontrollers'),
            ('ET105', 'Electronics Lab'),
            ('ET201', 'Signals and Systems'),
            ('ET202', 'Control Systems'),
            ('ET203', 'Communication Systems'),
            ('ET204', 'Microprocessors'),
            ('ET205', 'Telecommunication Lab'),
            # Second Year
            ('ET301', 'Advanced Circuit Design'),
            ('ET302', 'Embedded Systems'),
            ('ET303', 'VLSI Design'),
            ('ET304', 'Signal Processing'),
            ('ET305', 'Digital Signal Processing Lab'),
            ('ET401', 'Wireless Communication'),
            ('ET402', 'Optical Communication'),
            ('ET403', 'Control Theory'),
            ('ET404', 'Robotics'),
            ('ET405', 'Communication Lab'),
            # Third Year
            ('ET501', 'Radar Systems'),
            ('ET502', 'Advanced Embedded Systems'),
            ('ET503', 'Telematics'),
            ('ET504', 'Internet of Things'),
            ('ET505', 'Project Work'),
            ('ET601', 'Advanced Networking'),
            ('ET602', 'Machine Learning'),
            ('ET603', 'Smart Sensors'),
            ('ET604', 'Artificial Intelligence'),
            ('ET605', 'Research Project'),
            # Fourth Year
            ('ET701', 'Project Management'),
            ('ET702', 'Industry Internship'),
            ('ET703', 'Entrepreneurship'),
            ('ET704', 'Capstone Project'),
            ('ET705', 'Thesis'),
            ('ET801', 'Elective Course 1'),
            ('ET802', 'Elective Course 2'),
            ('ET803', 'Elective Course 3'),
            ('ET804', 'Elective Course 4'),
            ('ET805', 'Elective Course 5'),

            # Computer Science
            # First Year
            ('CS101', 'Introduction to Computer Science'),
            ('CS102', 'Data Structures'),
            ('CS103', 'Discrete Mathematics'),
            ('CS104', 'Computer Organization'),
            ('CS105', 'CS Lab'),
            ('CS201', 'Algorithms'),
            ('CS202', 'Operating Systems'),
            ('CS203', 'Database Systems'),
            ('CS204', 'Software Engineering'),
            ('CS205', 'DBMS Lab'),
            # Second Year
            ('CS301', 'Web Development'),
            ('CS302', 'Software Architecture'),
            ('CS303', 'Computer Networks'),
            ('CS304', 'Human-Computer Interaction'),
            ('CS305', 'Web Lab'),
            ('CS401', 'Mobile Application Development'),
            ('CS402', 'Cloud Computing'),
            ('CS403', 'Cyber Security'),
            ('CS404', 'Game Development'),
            ('CS405', 'Security Lab'),
            # Third Year
            ('CS501', 'Data Mining'),
            ('CS502', 'Machine Learning'),
            ('CS503', 'Big Data Analytics'),
            ('CS504', 'Blockchain Technology'),
            ('CS505', 'Project Work'),
            ('CS601', 'Advanced Databases'),
            ('CS602', 'Natural Language Processing'),
            ('CS603', 'Artificial Intelligence'),
            ('CS604', 'Computer Vision'),
            ('CS605', 'Research Project'),
            # Fourth Year
            ('CS701', 'Capstone Project'),
            ('CS702', 'Industry Internship'),
            ('CS703', 'Entrepreneurship'),
            ('CS704', 'Thesis'),
            ('CS705', 'Elective Course 1'),
            ('CS801', 'Elective Course 2'),
            ('CS802', 'Elective Course 3'),
            ('CS803', 'Elective Course 4'),
            ('CS804', 'Elective Course 5'),
            ('CS805', 'Elective Course 6'),

            # Information Technology
            # First Year
<<<<<<< HEAD
            ('IT101', 'Web Technologies'),
=======
            ('IT101', 'Web Technologies',True),
>>>>>>> c22b95e10b9996e1ebc994b1a1dbe55c94ce1b4d
            ('IT102', 'Network Fundamentals'),
            ('IT103', 'System Analysis'),
            ('IT104', 'Programming Fundamentals'),
            ('IT105', 'IT Lab'),
            ('IT201', 'Computer Networks'),
            ('IT202', 'Mobile Computing'),
            ('IT203', 'Software Testing'),
            ('IT204', 'Project Management'),
            ('IT205', 'Networking Lab'),
            # Second Year
            ('IT301', 'Information Security'),
            ('IT302', 'Web Application Development'),
            ('IT303', 'Data Analytics'),
            ('IT304', 'UI/UX Design'),
            ('IT305', 'Web Lab'),
            ('IT401', 'Cloud Computing'),
            ('IT402', 'Mobile Application Development'),
            ('IT403', 'E-Commerce'),
            ('IT404', 'DevOps'),
            ('IT405', 'Cloud Lab'),
            # Third Year
            ('IT501', 'Data Warehousing'),
            ('IT502', 'Artificial Intelligence'),
            ('IT503', 'Big Data'),
            ('IT504', 'Data Visualization'),
            ('IT505', 'Project Work'),
            ('IT601', 'Machine Learning'),
            ('IT602', 'IoT Systems'),
            ('IT603', 'Advanced Networking'),
            ('IT604', 'Information Retrieval'),
            ('IT605', 'Research Project'),
            # Fourth Year
            ('IT701', 'Capstone Project'),
            ('IT702', 'Industry Internship'),
            ('IT703', 'Entrepreneurship'),
            ('IT704', 'Thesis'),
            ('IT705', 'Elective Course 1'),
            ('IT801', 'Elective Course 2'),
            ('IT802', 'Elective Course 3'),
            ('IT803', 'Elective Course 4'),
            ('IT804', 'Elective Course 5'),
            ('IT805', 'Elective Course 6'),

            # Mechanical Engineering
            # First Year
            ('ME101', 'Engineering Mechanics'),
            ('ME102', 'Thermodynamics'),
            ('ME103', 'Fluid Mechanics'),
            ('ME104', 'Material Science'),
            ('ME105', 'Mechanical Lab'),
            ('ME201', 'Machine Design'),
            ('ME202', 'Manufacturing Processes'),
            ('ME203', 'Heat Transfer'),
            ('ME204', 'Production Engineering'),
            ('ME205', 'Manufacturing Lab'),
            # Second Year
            ('ME301', 'Mechanics of Materials'),
            ('ME302', 'Kinematics'),
            ('ME303', 'Thermal Engineering'),
            ('ME304', 'Fluid Machinery'),
            ('ME305', 'Lab Work'),
            ('ME401', 'Automobile Engineering'),
            ('ME402', 'Robotics'),
            ('ME403', 'Computer-Aided Design'),
            ('ME404', 'Production Management'),
            ('ME405', 'Robotics Lab'),
            # Third Year
            ('ME501', 'Design of Machine Elements'),
            ('ME502', 'Engineering Dynamics'),
            ('ME503', 'Advanced Manufacturing'),
            ('ME504', 'Thermal System Design'),
            ('ME505', 'Project Work'),
            ('ME601', 'Advanced Materials'),
            ('ME602', 'Energy Systems'),
            ('ME603', 'Automation'),
            ('ME604', 'Renewable Energy'),
            ('ME605', 'Research Project'),
            # Fourth Year
            ('ME701', 'Capstone Project'),
            ('ME702', 'Industry Internship'),
            ('ME703', 'Entrepreneurship'),
            ('ME704', 'Thesis'),
            ('ME705', 'Elective Course 1'),
            ('ME801', 'Elective Course 2'),
            ('ME802', 'Elective Course 3'),
            ('ME803', 'Elective Course 4'),
            ('ME804', 'Elective Course 5'),
            ('ME805', 'Elective Course 6'),
        ]
<<<<<<< HEAD

        for code, name in courses_data:
            try:
                course = Course(code=code, name=name)
=======
        for course_data in courses_data:
            try:
                # Unpack with a default value for `is_lab`
                if len(course_data) == 3:
                    code, name, is_lab = course_data
                else:
                    code, name = course_data
                    is_lab = False  # Default value if not provided
                
                course = Course(code=code, name=name, is_lab=is_lab)
>>>>>>> c22b95e10b9996e1ebc994b1a1dbe55c94ce1b4d
                course.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added course: {course}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding course: {e}'))
