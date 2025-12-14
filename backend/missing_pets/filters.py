
import django_filters
from .models import MissingPet


class MissingPetFilter(django_filters.FilterSet):
    """
    Advanced filters for Missing Pet reports
    
    Available filters:
    - category: Exact match (CAT, DOG, OTHER)
    - status: Exact match (MISSING, FOUND, CLOSED)
    - gender: Exact match (MALE, FEMALE, UNKNOWN)
    - last_seen_location: Case-insensitive contains search
    - breed: Case-insensitive contains search
    - name: Case-insensitive contains search
    - last_seen_after: Reports where pet was seen after this date
    - last_seen_before: Reports where pet was seen before this date
    - has_reward: Filter pets with reward offered
    
    Examples:
    - /api/v1/missing-pets/?category=DOG
    - /api/v1/missing-pets/?status=MISSING
    - /api/v1/missing-pets/?last_seen_location=Kathmandu
    - /api/v1/missing-pets/?last_seen_after=2025-01-01
    - /api/v1/missing-pets/?has_reward=true
    """
    
    # Location filter (case-insensitive partial match)
    last_seen_location = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Last seen location contains'
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
    
    # Date range filters
    last_seen_after = django_filters.DateFilter(
        field_name='last_seen_date',
        lookup_expr='gte',
        label='Last seen on or after'
    )
    last_seen_before = django_filters.DateFilter(
        field_name='last_seen_date',
        lookup_expr='lte',
        label='Last seen on or before'
    )
    
    # Has reward filter
    has_reward = django_filters.BooleanFilter(
        field_name='reward_offered',
        lookup_expr='isnull',
        exclude=True,
        label='Has reward offered'
    )
    
    class Meta:
        model = MissingPet
        fields = {
            'category': ['exact'],
            'status': ['exact'],
            'gender': ['exact'],
        }