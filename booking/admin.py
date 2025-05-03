from django.contrib import admin
from .models import Hotel

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']  # Fields to display in the list
    search_fields = ['name']  # Search by name
    list_filter = ['created_at']  # Filter by creation date