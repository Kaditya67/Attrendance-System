# Generated by Django 5.1.1 on 2024-09-22 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_semester_unique_together_alter_semester_year_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together={('session_year', 'semester_type')},
        ),
    ]
