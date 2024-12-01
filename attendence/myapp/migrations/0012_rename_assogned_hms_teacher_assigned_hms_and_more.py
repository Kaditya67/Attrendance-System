# Generated by Django 5.1.3 on 2024-12-01 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_teacher_assogned_hms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='assogned_hms',
            new_name='assigned_hms',
        ),
        migrations.AddField(
            model_name='honorsminors',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='honors_minors', to='myapp.student', verbose_name='Students'),
        ),
    ]
