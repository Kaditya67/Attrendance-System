from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('add_user/', views.add_user, name='add_user'),
    path('done/', views.done, name='done'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('principal_dashboard/', views.principal_dashboard, name='principal_dashboard'),
]
