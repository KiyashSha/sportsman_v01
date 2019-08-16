from django.contrib import admin
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('students_all/', views.students_all, name="students_all"),
    path('details/<int:student_admno>/', views.student_details, name="student_details"),
    path('add/',views.StudentCreate.as_view(), name="student_add"),
    path('upload/', views.bulk_upload, name="bulk_upload"),
    path('update/<int:pk>/',views.StudentUpdate.as_view(), name="student_update"),
    path('details/<int:student_admno>/add_sport/',views.add_sport, name="add_sport"),
    path('<int:student_admno>/delete/<int:sport_id>',views.delete_song, name="sport_delete")
]

#http://127.0.0.1:8000/student/detials/11485/
