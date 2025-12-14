from django.contrib import admin
from .models import TermsAndConditions, TermsAcceptance


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('version', 'effective_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'effective_date')
    search_fields = ('version', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Version Information', {
            'fields': ('version', 'effective_date', 'is_active')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        #Custom save to handle active version logic
        super().save_model(request, obj, form, change)
        if obj.is_active:
            # Deactivate all other versions
            TermsAndConditions.objects.exclude(id=obj.id).update(is_active=False)


@admin.register(TermsAcceptance)
class TermsAcceptanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'terms', 'accepted_at', 'ip_address')
    list_filter = ('accepted_at', 'terms')
    search_fields = ('user__email', 'user__full_name', 'ip_address')
    readonly_fields = ('user', 'terms', 'accepted_at', 'ip_address', 'user_agent')
    
    fieldsets = (
        ('User & Terms', {
            'fields': ('user', 'terms')
        }),
        ('Acceptance Details', {
            'fields': ('accepted_at', 'ip_address', 'user_agent')
        }),
    )
    
    def has_add_permission(self, request):
        #Disable manual creation - should be created programmatically
        return False
    
    def has_change_permission(self, request, obj=None):
        #Make read only
        return False