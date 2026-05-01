from django.contrib import admin
from .models import AnonymousPost

@admin.register(AnonymousPost)
class AnonymousPostAdmin(admin.ModelAdmin):
    list_display = ['token', 'created_at']
    readonly_fields = ['token']
