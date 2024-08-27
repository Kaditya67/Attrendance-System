from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('principal-dashboard/', views.principal_dashboard, name='principal_dashboard'),
]
