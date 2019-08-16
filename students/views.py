from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Student, Sport
from .forms import SportForm
import os

def students_all(request):
    template = 'students/profile_all.html'

    students = Student.objects.all()


    context = {
        'students' : students
    }

    return render(request, template, context)

def student_details(request, student_admno):
    template = 'students/profile_details.html'
    student = get_object_or_404(Student, student_admno=student_admno)
    context = {
        'student': student,
        }

    return render(request, template, context)

def add_sport(request,student_admno):
    form = SportForm(request.POST or None, request.FILES or None)
    student = get_object_or_404(Student, pk=student_admno)
    if form.is_valid():
        sport = form.save(commit=False)
        sport.student = student
        sport.save()

    if request.method == "POST":
        return HttpResponseRedirect(('/student/details/%d/'%student_admno))

    context = {
        'student': student,
        'form': form,
    }

    return render(request, 'students/sport_form.html', context)

def delete_song(request, student_admno, sport_id):
    student = get_object_or_404(Student, pk=student_admno)
    sport = Sport.objects.get(pk=sport_id)
    sport.delete()

    if request.method == "POST":
        return HttpResponseRedirect(('/student/details/%d/'%student_admno))

    return render(request, 'students/profile_details.html', {'student': student})

class StudentCreate(CreateView):
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

    template_name = 'students/student_create_form.html'

class StudentUpdate(UpdateView):
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

    template_name = 'students/student_update_form.html'
