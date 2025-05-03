from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)  # Hotel name
    description = models.TextField(blank=True, null=True)  # Description
    created_at = models.DateTimeField(auto_now_add=True)  # Creation date

    def __str__(self):
        return self.name