# Generated by Django 5.1.1 on 2024-09-22 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='name',
            field=models.CharField(choices=[('FE', 'First Year'), ('SE', 'Second Year'), ('TE', 'Third Year'), ('BE', 'Fourth Year')], max_length=10, verbose_name='Year'),
        ),
    ]
