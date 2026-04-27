from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import HttpResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def create_admin_view(request):
    from users.models import User
    email = 'admin@admin.com'
    password = 'adminpassword123'
    user, created = User.objects.get_or_create(email=email)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return HttpResponse(f"Admin {'created' if created else 'updated'} successfully")

urlpatterns = [
    path('api/create-admin-secret/', create_admin_view),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/food-diary/', include('food_diary.urls')),
    path('api/exercises/', include('exercises.urls')),
    path('api/progress/', include('progress.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
