from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

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
]