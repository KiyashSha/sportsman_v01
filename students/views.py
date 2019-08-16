from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Student, Sport
from .forms import SportForm
import os
import xlrd

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

def bulk_upload(request):
    template = 'students/bulk_upload.html'

    global html_msg, uploaded_file_url, sheet, num_students

    if request.method == 'POST' and 'submit_file' in request.POST:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location='media/uploads',base_url=os.path.join(settings.MEDIA_URL,'uploads'))
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, template, {
            'uploaded_file_url': uploaded_file_url
        })

    if "next" in request.POST:
        database_dir = os.path.join(settings.MEDIA_ROOT,'uploads')
        files = (os.listdir(database_dir))[0]
        filename = database_dir +'/'+ files
        database_loc = os.path.join(settings.MEDIA_ROOT,'uploads',filename)

        workbook = xlrd.open_workbook(database_loc)
        sheet = workbook.sheet_by_index(0)
        num_students = sheet.nrows-1

        html_msg = "You are about to Create %d New Student Profiles" %num_students

        context = {
            'uploaded_file_url': uploaded_file_url,
            'msg' : html_msg,
            }

        return render(request, template, context)

    if "execute" in request.POST:
        objects = []

        for i in range(num_students):
            i += 1
            row = sheet.row_values(i)

            admno = row[0]
            gender = row[1]
            classcode = row[2]
            fullname = row[3]
            first, *middle, last = fullname.split()

            middle_name = ""
            if not middle:
                middle_name = ""
            else:
                for n in middle:
                    middle_name = middle_name + n + " "
                middle_name = middle_name[:-1]

            objects.append(
                Student(
                    student_admno = admno,
                    student_gender = gender,
                    student_classcode = classcode,
                    student_fullname = fullname,
                    student_firstname = first,
                    student_middlename = middle_name,
                    student_lastname = last
                    )
                )

        Student.objects.bulk_create(objects)

        html_msg_1 = "%d New Student Profiles Created" %num_students
        context = {
            'uploaded_file_url': uploaded_file_url,
            'msg' : html_msg,
            'msg_1' : html_msg_1,
        }
        return render(request, template, context)


    return render(request, template,)

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
