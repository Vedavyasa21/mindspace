from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('wellness/', include('wellness.urls')),
    path('counseling/', include('counseling.urls')),
    path('support/', include('anonymous_support.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('streak/', include('streak.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
