from django.urls import path
from . import views

urlpatterns = [
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resources/create/', views.resource_create, name='resource_create'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('counselor-dashboard/', views.counselor_dashboard, name='counselor_dashboard'),
]
