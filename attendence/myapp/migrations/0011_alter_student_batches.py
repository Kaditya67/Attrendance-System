# Generated by Django 5.1.1 on 2024-09-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_semester_labs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='batches',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='Batches for Labs'),
        ),
    ]
