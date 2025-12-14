from django.db import models
from django.conf import settings
from django.utils import timezone


class TermsAndConditions(models.Model):
    #Model to store different versions of Terms & Conditions
    
    version = models.CharField(max_length=10, unique=True)
    content = models.TextField(help_text="Full Terms & Conditions text")
    effective_date = models.DateField()
    is_active = models.BooleanField(
        default=False,
        help_text="Only one version can be active at a time"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'terms_and_conditions'
        verbose_name = 'Terms and Conditions'
        verbose_name_plural = 'Terms and Conditions'
        ordering = ['-effective_date']
    
    def __str__(self):
        return f"Terms v{self.version} ({'Active' if self.is_active else 'Inactive'})"
    
    def save(self, *args, **kwargs):
        """Ensure only one version is active at a time"""
        if self.is_active:
            # Deactivate all other versions
            TermsAndConditions.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class TermsAcceptance(models.Model):
    #Model to track user acceptance of Terms & Conditions
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='terms_acceptances'
    )
    terms = models.ForeignKey(
        TermsAndConditions,
        on_delete=models.CASCADE,
        related_name='acceptances'
    )
    accepted_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(help_text="IP address when accepted")
    user_agent = models.TextField(
        blank=True,
        help_text="Browser/device information"
    )
    
    class Meta:
        db_table = 'terms_acceptance'
        verbose_name = 'Terms Acceptance'
        verbose_name_plural = 'Terms Acceptances'
        ordering = ['-accepted_at']
        # Prevent duplicate acceptances of same version
        unique_together = ('user', 'terms')
    
    def __str__(self):
        return f"{self.user.email} accepted v{self.terms.version} on {self.accepted_at.strftime('%Y-%m-%d')}"