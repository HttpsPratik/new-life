from django.db import models


class RescueContact(models.Model):
    #Model for shelter and veterinarian contacts
    
    TYPE_CHOICES = (
        ('SHELTER', 'Shelter'),
        ('VETERINARIAN', 'Veterinarian'),
    )
    
    # Basic information
    name = models.CharField(max_length=200, help_text="Name of shelter/clinic")
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    
    # Contact details
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    
    # Additional info
    description = models.TextField(blank=True, null=True)
    operating_hours = models.TextField(blank=True, null=True)
    
    # Shelter-specific fields
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Total capacity (for shelters)"
    )
    
    # Vet-specific fields
    specialization = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Specialization (for veterinarians)"
    )
    services = models.TextField(
        blank=True,
        null=True,
        help_text="Services offered (for veterinarians)"
    )
    emergency_service = models.BooleanField(
        default=False,
        help_text="24/7 emergency service available"
    )
    
    # Status
    is_verified = models.BooleanField(
        default=False,
        help_text="Verified by admin"
    )
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rescue_contacts'
        verbose_name = 'Rescue Contact'
        verbose_name_plural = 'Rescue Contacts'
        ordering = ['type', 'name']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['city']),
            models.Index(fields=['is_verified']),
        ]
    
    def __str__(self):
        verified = " ✓" if self.is_verified else ""
        return f"{self.name} ({self.get_type_display()}){verified}"