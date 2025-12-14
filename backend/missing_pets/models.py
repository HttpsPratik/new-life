from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class MissingPet(models.Model):
    """Model for missing pet reports"""
    
    CATEGORY_CHOICES = (
        ('CAT', 'Cat'),
        ('DOG', 'Dog'),
        ('OTHER', 'Other'),
    )
    
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('UNKNOWN', 'Unknown'),
    )
    
    STATUS_CHOICES = (
        ('MISSING', 'Missing'),
        ('FOUND', 'Found'),
        ('CLOSED', 'Closed'),
    )
    
    # Primary fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='missing_pet_reports'
    )
    
    # Pet information
    name = models.CharField(max_length=100, blank=True, null=True, help_text="Pet's name (if known)")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Missing details
    description = models.TextField(help_text="Distinctive features, markings, etc.")
    last_seen_location = models.CharField(max_length=200)
    last_seen_date = models.DateField()
    reward_offered = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Reward amount (if any)"
    )
    
    # Contact
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    
    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='MISSING')
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    found_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'missing_pets'
        verbose_name = 'Missing Pet Report'
        verbose_name_plural = 'Missing Pet Reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['last_seen_location']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        name = self.name or 'Unknown'
        return f"{name} ({self.category}) - {self.status}"
    
    def mark_as_found(self):
        #Mark pet as found
        self.status = 'FOUND'
        self.found_date = timezone.now()
        self.save(update_fields=['status', 'found_date'])


class MissingPetImage(models.Model):
    
    
    missing_pet = models.ForeignKey(
        MissingPet,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='missing_pets/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'missing_pet_images'
        verbose_name = 'Missing Pet Image'
        verbose_name_plural = 'Missing Pet Images'
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        name = self.missing_pet.name or 'Unknown'
        return f"Image for {name} {'(Primary)' if self.is_primary else ''}"
    
    def save(self, *args, **kwargs):
        #Ensure only one primary image per missing pet
        if self.is_primary:
            MissingPetImage.objects.filter(
                missing_pet=self.missing_pet,
                is_primary=True
            ).update(is_primary=False)
        super().save(*args, **kwargs)