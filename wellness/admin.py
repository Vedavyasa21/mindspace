from django.contrib import admin
from .models import WellnessResource

@admin.register(WellnessResource)
class WellnessResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'uploaded_by', 'is_active', 'created_at']
    list_filter = ['resource_type', 'is_active']
