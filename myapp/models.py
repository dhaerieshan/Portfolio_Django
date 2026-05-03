from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.received_at:%Y-%m-%d %H:%M}"
