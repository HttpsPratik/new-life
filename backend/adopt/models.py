from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Pet(models.Model):
    
    
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
    
    SIZE_CHOICES = (
        ('SMALL', 'Small'),
        ('MEDIUM', 'Medium'),
        ('LARGE', 'Large'),
    )
    
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('ADOPTED', 'Adopted'),
        ('PENDING', 'Pending'),
        ('REMOVED', 'Removed'),
    )
    
    # Primary fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pet_listings'
    )
    
    # Pet information
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(help_text="Age in months")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    
    # Description
    description = models.TextField()
    health_info = models.TextField(blank=True, null=True, help_text="Vaccination, medical history, etc.")
    
    # Location & Contact
    location = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    
    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    adoption_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'pets'
        verbose_name = 'Pet Listing'
        verbose_name_plural = 'Pet Listings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['location']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.category}) - {self.status}"
    
    def mark_as_adopted(self):
        #Mark pet as adopted
        self.status = 'ADOPTED'
        self.adoption_date = timezone.now()
        self.save(update_fields=['status', 'adoption_date'])


class PetImage(models.Model):
    #Model for pet images
    
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='pets/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'pet_images'
        verbose_name = 'Pet Image'
        verbose_name_plural = 'Pet Images'
        ordering = ['-is_primary', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.pet.name} {'(Primary)' if self.is_primary else ''}"
    
    def save(self, *args, **kwargs):
        #Ensure only one primary image per pet
        if self.is_primary:
            # Set all other images for this pet as non-primary
            PetImage.objects.filter(pet=self.pet, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)