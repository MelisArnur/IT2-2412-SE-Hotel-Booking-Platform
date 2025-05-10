from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name} ({self.check_in} to {self.check_out})"