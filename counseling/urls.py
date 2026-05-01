from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_session, name='book_session'),
    path('my-sessions/', views.my_sessions, name='my_sessions'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
]
