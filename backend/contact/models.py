from django.db import models
from django.conf import settings


class Feedback(models.Model):
    #Model for user feedback and contact messages
    
    TYPE_CHOICES = (
        ('FEEDBACK', 'Feedback'),
        ('BUG_REPORT', 'Bug Report'),
        ('SUGGESTION', 'Suggestion'),
        ('COMPLAINT', 'Complaint'),
        ('OTHER', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    
    # User (optional - can be anonymous)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedback'
    )
    
    # Contact information (for non-registered users)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    
    # Feedback details
    subject = models.CharField(max_length=200)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='FEEDBACK')
    message = models.TextField()
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='NEW')
    
    # Admin notes (internal use only)
    admin_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Internal notes (not visible to user)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'feedback'
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['type']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        sender = self.name or (self.user.full_name if self.user else 'Anonymous')
        return f"{sender} - {self.subject} ({self.status})"
    
    def get_sender_display(self):
        #Get sender name for display
        if self.user:
            return self.user.full_name
        return self.name or "Anonymous"