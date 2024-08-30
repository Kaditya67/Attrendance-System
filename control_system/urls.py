from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('add_user/', views.add_user, name='add_user'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('principal_dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('success/', views.success_page, name='success_page'),  # Add this if you have a success page
]
