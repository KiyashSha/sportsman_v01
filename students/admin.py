from django.contrib import admin
from .models import Student,Sport

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_admno', 'student_classcode', 'student_firstname', 'student_lastname')

admin.site.register(Student, StudentAdmin)
admin.site.register(Sport)
