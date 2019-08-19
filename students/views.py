from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
import os
import xlrd

from .models import Student, Sport
from .forms import SportForm, UserForm, StudentForm

def login_user(request):
    if request.user.is_authenticated:
        return redirect('students:students_all')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('students:students_all')
                else:
                    return render(request, 'students/login_form.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'students/login_form.html', {'error_message': 'Invalid login'})
        return render(request, 'students/login_form.html')

def students_all(request):
    if not request.user.is_authenticated:
        return render(request, 'students/login_form.html')
    else:
        template = 'students/profile_all.html'

        username = request.user.username
        students_all = Student.objects.all().order_by('student_grade','student_class_designation')

        page = request.GET.get('page')
        paginator = Paginator(students_all,30)

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        return render(request, 'students/profile_all.html',{'students': students, 'username': username, 'template': template})

def student_details(request, student_admno):
    if not request.user.is_authenticated:
        return render(request, 'students/login_form.html')
    else:
        username = request.user.username
        template = 'students/profile_details.html'
        student = get_object_or_404(Student, student_admno=student_admno)
        context = {
            'student': student,
            'template' : template,
            'username' : username
            }

        return render(request, template, context)

def add_sport(request,student_admno):
    if not request.user.is_authenticated:
        return render(request, 'students/login_form.html')
    else:
        username = request.user.username
        template = 'students/sport_form.html'
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
            'username': username,
            'template': template
        }

        return render(request, template, context)

def delete_sport(request, student_admno, sport_id):
    if not request.user.is_authenticated:
        return render(request, 'students/login_form.html')
    else:
        student = get_object_or_404(Student, pk=student_admno)
        sport = Sport.objects.get(pk=sport_id)
        sport.delete()

        if request.method == "POST":
            return HttpResponseRedirect(('/student/details/%d/'%student_admno))

        return render(request, 'students/profile_details.html', {'student': student})

def bulk_upload(request):
    if not request.user.is_authenticated:
        return render(request, 'students/login_form.html')
    else:
        template = 'students/bulk_upload.html'

        global html_msg, uploaded_file_url, sheet, num_students, database_loc

        if request.method == 'POST' and 'submit_file' in request.POST:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'uploads'),base_url=os.path.join(settings.MEDIA_URL,'uploads'))
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            database_loc = os.path.join(settings.MEDIA_ROOT,'uploads',filename)
            return render(request, template, {
                'uploaded_file_url': uploaded_file_url
            })

        if "next" in request.POST:
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
                if len(classcode) == 2:
                    grade = classcode[0]
                    class_designation = classcode[1]
                else:
                    grade = classcode[:2]
                    class_designation = classcode[2]

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
                        student_grade = grade,
                        student_class_designation = class_designation,
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

def create_student(request):
    if not request.user.is_authenticated:
        return render(request, 'students/login_form.html')
    else:
        username = request.user.username
        form = StudentForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            template = 'students/profile_details.html'
            return render(request, template, {'student':student, 'username':username, 'template': template})

    template = 'students/student_create_form.html'
    context = {
            "form": form,
            "username":username,
            'template': template
        }

    return render(request, template, context)

def update_student(request, student_admno):
    if not request.user.is_authenticated:
        return render(request, 'students/login_form.html')
    else:
        username = request.user.username
        student = Student.objects.get(pk=student_admno)
        if request.method =='POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                template = 'students/profile_details.html'
                return render(request, template, {'student':student, 'template':template})
            else:
                form = StudentForm(instance=student)
        else:
            form = StudentForm(instance=student)

        template = 'students/student_update_form.html'
        return render(request, template, {'form':form,'username':username, 'template':template})

def register_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('students:students_all')
    context = {
        "form": form,
    }
    return render(request, 'students/registration_form.html', context)

def logout_user(request):
    logout(request)

    return redirect('login_user')
