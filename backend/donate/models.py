from django.db import models
from django.conf import settings
import uuid


class Donation(models.Model):
    
    PAYMENT_METHOD_CHOICES = (
        ('ESEWA', 'eSewa'),
        ('PAYPAL', 'PayPal'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )
    
    CURRENCY_CHOICES = (
        ('NPR', 'Nepalese Rupee'),
        ('USD', 'US Dollar'),
    )
    
    # Primary fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations',
        help_text="Leave blank for anonymous donations"
    )
    
    # Donor information (for non-registered donors)
    donor_name = models.CharField(max_length=200, blank=True, null=True)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Donation details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NPR')
    
    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_reference = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Transaction ID from payment gateway"
    )
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )
    
    # Additional info
    message = models.TextField(
        blank=True,
        null=True,
        help_text="Optional message from donor"
    )
    is_anonymous = models.BooleanField(
        default=False,
        help_text="Hide donor name from public display"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When payment was confirmed"
    )
    
    class Meta:
        db_table = 'donations'
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_status']),
            models.Index(fields=['payment_method']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        donor = self.donor_name or (self.donor.full_name if self.donor else 'Anonymous')
        return f"{donor} - {self.currency} {self.amount} ({self.payment_status})"
    
    def get_donor_display_name(self):
        #Get donor name for display (respects anonymity)
        if self.is_anonymous:
            return "Anonymous"
        return self.donor_name or (self.donor.full_name if self.donor else "Anonymous")