from django.urls import path
from . import views

urlpatterns = [
    path('progress/', views.progress_view, name='progress'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
]
