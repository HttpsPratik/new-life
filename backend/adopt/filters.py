
import django_filters
from .models import Pet


class PetFilter(django_filters.FilterSet):
    """
    Advanced filters for Pet listings
    
    Available filters:
    - category: Exact match (CAT, DOG, OTHER)
    - location: Case-insensitive contains search
    - status: Exact match (AVAILABLE, ADOPTED, PENDING, REMOVED)
    - gender: Exact match (MALE, FEMALE, UNKNOWN)
    - size: Exact match (SMALL, MEDIUM, LARGE)
    - age_min: Minimum age in months
    - age_max: Maximum age in months
    - breed: Case-insensitive contains search
    - name: Case-insensitive contains search
    
    Examples:
    - /api/v1/pets/?category=DOG
    - /api/v1/pets/?location=Kathmandu
    - /api/v1/pets/?age_min=12&age_max=36
    - /api/v1/pets/?category=CAT&location=Pokhara
    """
    
    # Age range filters
    age_min = django_filters.NumberFilter(
        field_name='age',
        lookup_expr='gte',
        label='Minimum age (months)'
    )
    age_max = django_filters.NumberFilter(
        field_name='age',
        lookup_expr='lte',
        label='Maximum age (months)'
    )
    
    # Location filter (case-insensitive partial match)
    location = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Location contains'
    )
    
    # Breed filter (case-insensitive partial match)
    breed = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Breed contains'
    )
    
    # Name filter (case-insensitive partial match)
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Name contains'
    )
    
    class Meta:
        model = Pet
        fields = {
            'category': ['exact'],
            'status': ['exact'],
            'gender': ['exact'],
            'size': ['exact'],
        }