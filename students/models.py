from django.db import models
from django.urls import reverse

class Student(models.Model):
    student_admno = models.IntegerField(primary_key=True, verbose_name='Admin Number')
    student_gender = models.CharField(max_length=10, verbose_name='Gender')
    student_classcode = models.CharField(max_length=10, verbose_name='Class Code')
    student_fullname = models.CharField(max_length=200, verbose_name='Full Name')
    student_firstname = models.CharField(max_length=50, verbose_name='First Name')
    student_middlename = models.CharField(max_length=50, blank=True, verbose_name='Middle Name')
    student_lastname = models.CharField(max_length=50, verbose_name='Last Name')

    def get_absolute_url(self):
        return reverse('students:student_details', kwargs={'student_admno':self.student_admno})

    def __str__(self):
        return str(self.student_admno)


class Sport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sport_played = models.CharField(max_length=100, verbose_name='Sport Name')
    achievement = models.CharField(max_length=100, verbose_name='Students Achievement')
    year_participated = models.IntegerField(verbose_name='Year Participated')

    def __str__(self):
        return self.sport_played
