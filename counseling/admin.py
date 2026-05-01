from django.contrib import admin
from .models import CounselingSession

@admin.register(CounselingSession)
class CounselingSessionAdmin(admin.ModelAdmin):
    list_display = ['student', 'counselor', 'date', 'status', 'created_at']
    list_filter = ['status']
