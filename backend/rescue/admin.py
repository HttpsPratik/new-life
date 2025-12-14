from django.contrib import admin
from .models import RescueContact


@admin.register(RescueContact)
class RescueContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'city', 'phone', 'is_verified', 'is_active', 'created_at')
    list_filter = ('type', 'is_verified', 'is_active', 'city', 'emergency_service')
    search_fields = ('name', 'city', 'address', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'type', 'description')
        }),
        ('Location', {
            'fields': ('address', 'city')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'website', 'operating_hours')
        }),
        ('Shelter-Specific', {
            'fields': ('capacity',),
            'classes': ('collapse',),
            'description': 'Only for shelters'
        }),
        ('Veterinarian-Specific', {
            'fields': ('specialization', 'services', 'emergency_service'),
            'classes': ('collapse',),
            'description': 'Only for veterinarians'
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['verify_contacts', 'unverify_contacts', 'activate_contacts', 'deactivate_contacts']
    
    def verify_contacts(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f'{count} contact(s) verified.')
    verify_contacts.short_description = 'Verify selected contacts'
    
    def unverify_contacts(self, request, queryset):
        count = queryset.update(is_verified=False)
        self.message_user(request, f'{count} contact(s) unverified.')
    unverify_contacts.short_description = 'Unverify selected contacts'
    
    def activate_contacts(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} contact(s) activated.')
    activate_contacts.short_description = 'Activate selected contacts'
    
    def deactivate_contacts(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} contact(s) deactivated.')
    deactivate_contacts.short_description = 'Deactivate selected contacts'