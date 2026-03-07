from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/food-diary/', include('food_diary.urls')),
    path('api/exercises/', include('exercises.urls')),
    path('api/progress/', include('progress.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
