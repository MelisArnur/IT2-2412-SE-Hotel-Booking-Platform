from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    