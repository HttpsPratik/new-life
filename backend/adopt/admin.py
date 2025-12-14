from django.contrib import admin
from .models import Pet, PetImage
from django.utils import timezone


class PetImageInline(admin.TabularInline):
    """Inline admin for pet images"""
    model = PetImage
    extra = 1
    readonly_fields = ('uploaded_at',)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'breed', 'owner', 'location', 'status', 'created_at')
    list_filter = ('category', 'status', 'gender', 'size', 'location', 'created_at')
    search_fields = ('name', 'breed', 'description', 'owner__email', 'owner__full_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'adoption_date')
    inlines = [PetImageInline]
    
    fieldsets = (
        ('Owner', {
            'fields': ('owner',)
        }),
        ('Pet Information', {
            'fields': ('name', 'category', 'breed', 'age', 'gender', 'size')
        }),
        ('Description', {
            'fields': ('description', 'health_info')
        }),
        ('Location & Contact', {
            'fields': ('location', 'contact_phone', 'contact_email')
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'adoption_date')
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_adopted', 'mark_as_available', 'deactivate_listings']
    
    def mark_as_adopted(self, request, queryset):
        """Bulk action to mark pets as adopted"""
        count = queryset.update(status='ADOPTED', adoption_date=timezone.now())
        self.message_user(request, f'{count} pet(s) marked as adopted.')
    mark_as_adopted.short_description = 'Mark selected pets as adopted'
    
    def mark_as_available(self, request, queryset):
        """Bulk action to mark pets as available"""
        count = queryset.update(status='AVAILABLE')
        self.message_user(request, f'{count} pet(s) marked as available.')
    mark_as_available.short_description = 'Mark selected pets as available'
    
    def deactivate_listings(self, request, queryset):
        """Bulk action to deactivate listings"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} listing(s) deactivated.')
    deactivate_listings.short_description = 'Deactivate selected listings'


@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    list_display = ('pet', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('pet__name',)
    readonly_fields = ('uploaded_at',)