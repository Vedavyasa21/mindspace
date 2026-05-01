from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_anonymous, name='post_anonymous'),
    path('posts/', views.anonymous_posts, name='anonymous_posts'),
    path('respond/<int:pk>/', views.respond_to_post, name='respond_to_post'),
]
