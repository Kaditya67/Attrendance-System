from django.contrib import admin
from django.urls import path

from .views import update_permissions, permission_denied, manage_permissions

urlpatterns = [
    path('manage_permissions/', manage_permissions, name='manage_permissions'),
    path('update_permissions/', update_permissions, name='update_permissions'),
    path('permission_denied/', permission_denied, name='permission_denied'),
]
