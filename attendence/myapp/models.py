from django.db import models

# Create your models here.

class Year(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    def _str_(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    labs_batches = models.ForeignKey('LabsBatches', on_delete=models.SET_NULL, null=True, blank=True)
    odd_sem = models.ForeignKey('OddSem', on_delete=models.SET_NULL, null=True, blank=True)
    even_sem = models.ForeignKey('EvenSem', on_delete=models.SET_NULL, null=True, blank=True)
    honors_minors = models.ForeignKey('HonorsMinors', on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True, blank=True)
    honors_minors = models.ForeignKey('HonorsMinors', on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return self.name


class HonorsMinors(models.Model):
    name = models.CharField(max_length=100)
    even_sem = models.ForeignKey('EvenSem', on_delete=models.CASCADE)
    odd_sem = models.ForeignKey('OddSem', on_delete=models.CASCADE)

    def _str_(self):
        return self.name
    
class EvenSem(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)

    def _str_(self):
        return f"Even Sem {self.id} - {self.department.name}"


class OddSem(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)

    def _str_(self):
        return f"Odd Sem {self.id} - {self.department.name}"


class Program(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10)

    def _str_(self):
        return f"{self.name} - {self.semester}"

class Lecture(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def _str_(self):
        return f"Lecture for {self.program.name} - Student {self.student.name}"


class LabsBatches(models.Model):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def _str_(self):
        return f"Lab Batch {self.name} - Program {self.program.name}"