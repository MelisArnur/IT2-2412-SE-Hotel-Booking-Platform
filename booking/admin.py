from django.contrib import admin
from .models import Hotel, Booking, HotelImage, Review, Room
from django.utils.html import format_html

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    fields = ('room_number', 'room_type', 'price_per_night', 'beds', 'area', 'has_balcony', 'view', 'image')  # Добавляем поле image

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'location', 'latitude', 'longitude']
    list_filter = ['wifi', 'parking', 'pool', 'restaurant', 'gym']
    inlines = [HotelImageInline, RoomInline]
    search_fields = ['name', 'location']

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'location', 'rating', 'wifi', 'parking', 'pool', 'restaurant', 'gym', 'cancellation_policy', 'nearby_attractions')
        }),
        ('Location Coordinates', {
            'fields': ('latitude', 'longitude'),
            'description': 'Enter latitude and longitude manually. Use a service like https://www.latlong.net/ to find coordinates.'
        }),
    )

    def map_preview(self, obj):
        if obj.latitude and obj.longitude:
            return format_html(
                '''
                <div id="map-{id}" style="height: 400px; width: 600px;"></div>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {{
                        var map = L.map("map-{id}").setView([{lat}, {lng}], 15);
                        L.tileLayer("https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
                            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        }}).addTo(map);
                        L.marker([{lat}, {lng}]).addTo(map)
                            .bindPopup("{name}")
                            .openPopup();
                    }});
                </script>
                ''',
                id=obj.id, lat=obj.latitude, lng=obj.longitude, name=obj.name
            )
        return "No map available"
    map_preview.short_description = "Map Preview"
    list_display += ('map_preview',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'user', 'room', 'check_in', 'check_out', 'created_at']
    list_filter = ['check_in', 'check_out', 'created_at']

@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'image']
    list_filter = ['hotel']
    search_fields = ['hotel__name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'user', 'rating', 'comment', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['hotel__name', 'user__username']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'room_number', 'room_type', 'price_per_night', 'beds', 'area', 'has_balcony', 'view', 'image']
    list_filter = ['hotel', 'room_type', 'has_balcony']
    search_fields = ['hotel__name', 'room_number']