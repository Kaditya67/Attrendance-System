from django.contrib import admin

# Register your models here.
import myapp.models as models 


admin.site.register(models.Department)
admin.site.register(models.Year)
admin.site.register(models.Program)
admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.OddSem)
admin.site.register(models.EvenSem)
admin.site.register(models.HonorsMinors)
admin.site.register(models.LabsBatches)
admin.site.register(models.Lecture)