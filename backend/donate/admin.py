from django.contrib import admin
from django.utils import timezone
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('get_donor_name', 'amount', 'currency', 'payment_method', 
                    'payment_status', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'currency', 'is_anonymous', 'created_at')
    search_fields = ('donor_name', 'donor_email', 'donor__email', 'donor__full_name', 
                     'payment_reference')
    readonly_fields = ('id', 'created_at', 'updated_at', 'completed_at')
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor', 'donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'currency', 'message')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_reference', 'payment_status', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_success', 'mark_as_failed', 'mark_as_refunded']
    
    def get_donor_name(self, obj):
        #Display donor name in list
        return obj.get_donor_display_name()
    get_donor_name.short_description = 'Donor'
    
    def mark_as_success(self, request, queryset):
        #Bulk action to mark donations as successful
        count = queryset.update(payment_status='SUCCESS', completed_at=timezone.now())
        self.message_user(request, f'{count} donation(s) marked as successful.')
    mark_as_success.short_description = 'Mark as successful'
    
    def mark_as_failed(self, request, queryset):
        #Bulk action to mark donations as failed
        count = queryset.update(payment_status='FAILED')
        self.message_user(request, f'{count} donation(s) marked as failed.')
    mark_as_failed.short_description = 'Mark as failed'
    
    def mark_as_refunded(self, request, queryset):
        #Bulk action to mark donations as refunded
        count = queryset.update(payment_status='REFUNDED')
        self.message_user(request, f'{count} donation(s) marked as refunded.')
    mark_as_refunded.short_description = 'Mark as refunded'