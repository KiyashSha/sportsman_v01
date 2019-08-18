from django.contrib import admin
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('register-user', views.register_user, name='register_user'),
    path('logout-user', views.logout_user, name='logout_user'),
    path('students-all/', views.students_all, name="students_all"),
    path('details/<int:student_admno>/', views.student_details, name="student_details"),
    path('add/',views.create_student, name="create_student"),
    path('upload/', views.bulk_upload, name="bulk_upload"),
    path('update/<int:student_admno>/',views.update_student, name="student_update"),
    path('details/<int:student_admno>/add_sport/',views.add_sport, name="add_sport"),
    path('<int:student_admno>/delete/<int:sport_id>',views.delete_sport, name="sport_delete")
]

#http://127.0.0.1:8000/student/detials/11485/
