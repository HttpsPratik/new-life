from django.contrib import admin
from django.utils import timezone
from .models import MissingPet, MissingPetImage


class MissingPetImageInline(admin.TabularInline):
    """Inline admin for missing pet images"""
    model = MissingPetImage
    extra = 1
    readonly_fields = ('uploaded_at',)


@admin.register(MissingPet)
class MissingPetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'reporter', 'last_seen_location', 'status', 'created_at')
    list_filter = ('category', 'status', 'gender', 'last_seen_date', 'created_at')
    search_fields = ('name', 'breed', 'description', 'last_seen_location', 
                     'reporter__email', 'reporter__full_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'found_date')
    inlines = [MissingPetImageInline]
    
    fieldsets = (
        ('Reporter', {
            'fields': ('reporter',)
        }),
        ('Pet Information', {
            'fields': ('name', 'category', 'breed', 'gender')
        }),
        ('Missing Details', {
            'fields': ('description', 'last_seen_location', 'last_seen_date', 'reward_offered')
        }),
        ('Contact', {
            'fields': ('contact_phone', 'contact_email')
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'found_date')
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_found', 'mark_as_missing', 'close_reports']
    
    def mark_as_found(self, request, queryset):
        """Bulk action to mark pets as found"""
        count = queryset.update(status='FOUND', found_date=timezone.now())
        self.message_user(request, f'{count} pet(s) marked as found.')
    mark_as_found.short_description = 'Mark selected pets as found'
    
    def mark_as_missing(self, request, queryset):
        """Bulk action to mark pets as missing"""
        count = queryset.update(status='MISSING')
        self.message_user(request, f'{count} pet(s) marked as missing.')
    mark_as_missing.short_description = 'Mark selected pets as missing'
    
    def close_reports(self, request, queryset):
        """Bulk action to close reports"""
        count = queryset.update(status='CLOSED', is_active=False)
        self.message_user(request, f'{count} report(s) closed.')
    close_reports.short_description = 'Close selected reports'


@admin.register(MissingPetImage)
class MissingPetImageAdmin(admin.ModelAdmin):
    list_display = ('missing_pet', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('missing_pet__name',)
    readonly_fields = ('uploaded_at',)