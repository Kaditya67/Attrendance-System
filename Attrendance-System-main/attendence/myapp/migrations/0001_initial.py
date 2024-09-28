# Generated by Django 5.1.1 on 2024-09-28 07:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Course Code')),
                ('name', models.CharField(max_length=100, verbose_name='Course Name')),
                ('is_lab', models.BooleanField(default=False, verbose_name='Is Lab')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Department Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'indexes': [models.Index(fields=['name'], name='myapp_depar_name_7489d7_idx')],
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Program Name')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='myapp.department', verbose_name='Department')),
            ],
        ),
        migrations.CreateModel(
            name='LabsBatches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Batch Name')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labs_batches', to='myapp.department', verbose_name='Department')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labs_batches', to='myapp.program', verbose_name='Program')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.IntegerField(verbose_name='Semester Number')),
                ('semester_type', models.CharField(choices=[('Odd', 'Odd'), ('Even', 'Even')], max_length=10, verbose_name='Semester Type')),
                ('year', models.CharField(choices=[('FE', 'First Year'), ('SE', 'Second Year'), ('TE', 'Third Year'), ('BE', 'Fourth Year')], max_length=2, verbose_name='Year')),
                ('courses', models.ManyToManyField(blank=True, related_name='semesters', to='myapp.course', verbose_name='Courses')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('time_slot', models.CharField(choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')], max_length=20, verbose_name='Time Slot')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='myapp.course', verbose_name='Course')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='myapp.program', verbose_name='Program')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='myapp.semester', verbose_name='Semester')),
            ],
        ),
        migrations.CreateModel(
            name='HonorsMinors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Honors/Minors Name')),
                ('semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='honors_minors', to='myapp.semester', verbose_name='Semester')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_list', to='myapp.semester', verbose_name='Semester'),
        ),
        migrations.CreateModel(
            name='SessionYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.CharField(max_length=10, verbose_name='Academic Year')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='myapp.department', verbose_name='Department')),
            ],
        ),
        migrations.AddField(
            model_name='semester',
            name='session_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semesters', to='myapp.sessionyear', verbose_name='Session Year'),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100, verbose_name='Position')),
                ('staff_id', models.CharField(max_length=10, unique=True, verbose_name='Staff ID')),
                ('assigned_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff', to='myapp.department', verbose_name='Assigned Department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=20, unique=True, verbose_name='Student ID')),
                ('roll_number', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Roll Number')),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile Number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('lab_batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.labsbatches', verbose_name='Lab Batch')),
                ('semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='myapp.semester', verbose_name='Semester')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SemesterCGPA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cgpa', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='CGPA')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_cgpas', to='myapp.semester', verbose_name='Semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_cgpas', to='myapp.student', verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='myapp.course', verbose_name='Course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='myapp.semester', verbose_name='Semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='myapp.student', verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('time_slot', models.CharField(blank=True, choices=[('8-9', '8:00 AM - 9:00 AM'), ('9-10', '9:00 AM - 10:00 AM'), ('10-11', '10:00 AM - 11:00 AM'), ('11:15-12:15', '11:15 AM - 12:15 PM'), ('12:15-1:15', '12:15 PM - 1:15 PM'), ('2-3', '2:00 PM - 3:00 PM'), ('3-4', '3:00 PM - 4:00 PM'), ('4-5', '4:00 PM - 5:00 PM')], max_length=20, null=True, verbose_name='Time Slot')),
                ('present', models.BooleanField(default=False, verbose_name='Present')),
                ('count', models.IntegerField(blank=True, default=0, null=True, verbose_name='Count')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='myapp.course', verbose_name='Course')),
                ('lab_batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.labsbatches', verbose_name='Lab Batch')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='myapp.student', verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_id', models.CharField(max_length=10, unique=True, verbose_name='Faculty ID')),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile Number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('experience', models.TextField(blank=True, null=True, verbose_name='Experience')),
                ('assigned_courses', models.ManyToManyField(blank=True, related_name='assigned_teachers', to='myapp.course', verbose_name='Assigned Courses')),
                ('courses_taught', models.ManyToManyField(blank=True, related_name='teachers', to='myapp.course', verbose_name='Courses Taught')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teachers', to='myapp.department', verbose_name='Department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HOD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Office Number')),
                ('managing_teachers', models.IntegerField(verbose_name='Managing Teachers')),
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FE', 'First Year'), ('SE', 'Second Year'), ('TE', 'Third Year'), ('BE', 'Fourth Year')], max_length=10, verbose_name='Year')),
            ],
            options={
                'indexes': [models.Index(fields=['name'], name='myapp_year_name_7bff85_idx')],
            },
        ),
        migrations.AddField(
            model_name='program',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='myapp.year', verbose_name='Year'),
        ),
        migrations.CreateModel(
            name='Principal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office_location', models.CharField(default='Unknown Location', max_length=255, verbose_name='Office Location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_view_principal', 'Can view Principal details')],
                'indexes': [models.Index(fields=['office_location'], name='myapp_princ_office__f87ced_idx')],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('STUDENT', 'Student'), ('TEACHER', 'Teacher'), ('STAFF', 'Staff'), ('HOD', 'HOD'), ('PRINCIPAL', 'Principal')], default='STUDENT', max_length=20, verbose_name='User Type')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user_type'], name='myapp_profi_user_ty_40bb3b_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='labsbatches',
            index=models.Index(fields=['name'], name='myapp_labsb_name_c1db7f_idx'),
        ),
        migrations.AddIndex(
            model_name='lecture',
            index=models.Index(fields=['date'], name='myapp_lectu_date_2bacda_idx'),
        ),
        migrations.AddIndex(
            model_name='lecture',
            index=models.Index(fields=['time_slot'], name='myapp_lectu_time_sl_d84722_idx'),
        ),
        migrations.AddIndex(
            model_name='lecture',
            index=models.Index(fields=['date', 'time_slot'], name='myapp_lectu_date_732299_idx'),
        ),
        migrations.AddIndex(
            model_name='honorsminors',
            index=models.Index(fields=['name'], name='myapp_honor_name_87bd36_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['code'], name='myapp_cours_code_389fc6_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['name'], name='myapp_cours_name_d4e38d_idx'),
        ),
        migrations.AddIndex(
            model_name='sessionyear',
            index=models.Index(fields=['academic_year'], name='myapp_sessi_academi_42980d_idx'),
        ),
        migrations.AddIndex(
            model_name='sessionyear',
            index=models.Index(fields=['start_date'], name='myapp_sessi_start_d_c8a4c1_idx'),
        ),
        migrations.AddIndex(
            model_name='sessionyear',
            index=models.Index(fields=['end_date'], name='myapp_sessi_end_dat_4439ab_idx'),
        ),
        migrations.AddIndex(
            model_name='semester',
            index=models.Index(fields=['semester_number'], name='myapp_semes_semeste_2591cc_idx'),
        ),
        migrations.AddIndex(
            model_name='semester',
            index=models.Index(fields=['semester_type'], name='myapp_semes_semeste_7ff5a1_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together={('session_year', 'semester_number')},
        ),
        migrations.AddIndex(
            model_name='staff',
            index=models.Index(fields=['staff_id'], name='myapp_staff_staff_i_4202da_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['student_id'], name='myapp_stude_student_f849be_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['roll_number'], name='myapp_stude_roll_nu_08e2c0_idx'),
        ),
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['email'], name='myapp_stude_email_55f668_idx'),
        ),
        migrations.AddIndex(
            model_name='semestercgpa',
            index=models.Index(fields=['semester'], name='myapp_semes_semeste_6e9236_idx'),
        ),
        migrations.AddIndex(
            model_name='semestercgpa',
            index=models.Index(fields=['cgpa'], name='myapp_semes_cgpa_4f9f34_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='semestercgpa',
            unique_together={('student', 'semester')},
        ),
        migrations.AddIndex(
            model_name='enrollment',
            index=models.Index(fields=['student'], name='myapp_enrol_student_d372db_idx'),
        ),
        migrations.AddIndex(
            model_name='enrollment',
            index=models.Index(fields=['course'], name='myapp_enrol_course__33fe2a_idx'),
        ),
        migrations.AddIndex(
            model_name='enrollment',
            index=models.Index(fields=['semester'], name='myapp_enrol_semeste_d28fdd_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together={('student', 'course', 'semester')},
        ),
        migrations.AddIndex(
            model_name='attendance',
            index=models.Index(fields=['date'], name='myapp_atten_date_d4e8eb_idx'),
        ),
        migrations.AddIndex(
            model_name='attendance',
            index=models.Index(fields=['present'], name='myapp_atten_present_a3bc02_idx'),
        ),
        migrations.AddIndex(
            model_name='attendance',
            index=models.Index(fields=['date', 'time_slot'], name='myapp_atten_date_e37ae6_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('student', 'course', 'date', 'lab_batch')},
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['faculty_id'], name='myapp_teach_faculty_695d97_idx'),
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['mobile_no'], name='myapp_teach_mobile__fe8c3c_idx'),
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['email'], name='myapp_teach_email_9ccb9c_idx'),
        ),
        migrations.AddIndex(
            model_name='program',
            index=models.Index(fields=['name'], name='myapp_progr_name_331be0_idx'),
        ),
    ]
