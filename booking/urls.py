from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from rest_framework.routers import DefaultRouter  # Убедимся, что импорт есть

router = DefaultRouter()
router.register(r'hotels', views.HotelViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/create/', views.HotelCreateView.as_view(), name='hotel-create'),
    path('hotels/<int:pk>/update/', views.HotelUpdateView.as_view(), name='hotel-update'),
    path('hotels/<int:pk>/delete/', views.HotelDeleteView.as_view(), name='hotel-delete'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('bookings/', views.booking_list, name='booking-list'),
    path('bookings/create/', views.booking_create, name='booking-create'),
    path('api/', include(router.urls)),  # Используем router.urls
]