from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),               # админ-панель Django
    path('', include('courses.urls')),             # подключаем маршруты приложения courses
]

# Добавляем обработку медиа-файлов только в режиме отладки (разработка)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)