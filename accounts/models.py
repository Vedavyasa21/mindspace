from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('counselor', 'Counselor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    specialization = models.CharField(max_length=100, blank=True, help_text="For counselors only")

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_student(self):
        return self.role == 'student'

    def is_counselor(self):
        return self.role == 'counselor'

    def is_admin_user(self):
        return self.role == 'admin'
