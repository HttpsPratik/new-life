"""
Main API URL Configuration
All API endpoints are under /api/v1/
"""
from django.urls import path, include

urlpatterns = [
    # Authentication endpoints
    path('auth/', include('users.urls')),
    
    # Terms & Conditions endpoints
    path('terms/', include('terms.urls')),
    
    # Pet adoption endpoints
    path('pets/', include('adopt.urls')),
    
    # Missing pets endpoints
    path('missing-pets/', include('missing_pets.urls')),
    
    # Rescue contacts (shelters & vets) endpoints
    path('rescue/', include('rescue.urls')),
    
    # Donation endpoints
    path('donations/', include('donate.urls')),
    
    # Feedback/Contact endpoints
    path('feedback/', include('contact.urls')),
]