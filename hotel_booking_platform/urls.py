from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Обрабатываем POST-запрос от формы смены языка
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Основные маршруты (с префиксом языка)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
    prefix_default_language=True,
)

# Статика и медиа
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
