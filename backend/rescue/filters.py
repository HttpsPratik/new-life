import django_filters
from .models import RescueContact


class RescueContactFilter(django_filters.FilterSet):
    """
    Advanced filters for Rescue Contacts
    
    Available filters:
    - type: Exact match (SHELTER, VETERINARIAN)
    - city: Case-insensitive contains search
    - is_verified: Boolean (true/false)
    - emergency_service: Boolean (true/false) - for vets only
    - name: Case-insensitive contains search
    
    Examples:
    - /api/v1/rescue/?type=SHELTER
    - /api/v1/rescue/?type=VETERINARIAN
    - /api/v1/rescue/?city=Kathmandu
    - /api/v1/rescue/?is_verified=true
    - /api/v1/rescue/?type=VETERINARIAN&emergency_service=true
    """
    
    # City filter (case-insensitive partial match)
    city = django_filters.CharFilter(
        lookup_expr='icontains',
        label='City contains'
    )
    
    # Name filter (case-insensitive partial match)
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Name contains'
    )
    
    class Meta:
        model = RescueContact
        fields = {
            'type': ['exact'],
            'is_verified': ['exact'],
            'emergency_service': ['exact'],
        }