"""
Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


def home_view(request):
    """Homepage view that shows API information"""
    return JsonResponse({
        'message': 'Welcome to Pet Adoption & Rescue API',
        'version': '1.0.0',
        'endpoints': {
            'api_root': '/api/v1/',
            'admin': '/admin/',
            'documentation': '/api/docs/',
            'schema': '/api/schema/',
            'redoc': '/api/redoc/',
        },
        'available_apis': {
            'auth': '/api/v1/auth/',
            'pets': '/api/v1/pets/',
            'missing_pets': '/api/v1/missing-pets/',
            'rescue': '/api/v1/rescue/',
            'donations': '/api/v1/donations/',
            'feedback': '/api/v1/feedback/',
            'terms': '/api/v1/terms/',
        }
    })


urlpatterns = [
    # Homepage
    path('', home_view, name='home'),
    
    # Admin site
    path('admin/', admin.site.urls),
    
    # API v1 endpoints
    path('api/v1/', include('root.api_urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)