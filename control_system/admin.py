from django.contrib import admin

# Register your models here.
from .models import Student, Teacher, Principal

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Principal)
