from django.db import models
from accounts.models import CustomUser

class WellnessResource(models.Model):
    TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('tip', 'Tip'),
        ('exercise', 'Exercise'),
    ]
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content = models.TextField()
    url = models.URLField(blank=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
