from django import forms
from django.contrib.auth.models import User

from .models import Student, Sport

class SportForm(forms.ModelForm):

    class Meta:
        model = Sport
        fields = ('sport_played','achievement','year_participated')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email', 'password']

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'student_admno',
            'student_gender',
            'student_classcode',
            'student_fullname',
            'student_firstname',
            'student_middlename',
            'student_lastname'
            ]
