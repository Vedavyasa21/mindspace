import uuid
from django.db import models
from accounts.models import CustomUser

class AnonymousPost(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    message = models.TextField()
    response = models.TextField(blank=True)
    responded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Post {str(self.token)[:8]} - {'Resolved' if self.is_resolved else 'Open'}"

    class Meta:
        ordering = ['-created_at']
