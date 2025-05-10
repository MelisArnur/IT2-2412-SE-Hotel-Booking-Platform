from django.contrib import admin
from .models import Hotel, Booking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']  # Убери created_at, так как его нет
    list_filter = []                        # Очисти, если там был created_at

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'user', 'check_in', 'check_out', 'created_at']
    list_filter = ['check_in', 'check_out', 'created_at']