from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('get_sender', 'subject', 'type', 'status', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('subject', 'message', 'name', 'email', 'user__email', 'user__full_name')
    readonly_fields = ('user', 'name', 'email', 'subject', 'type', 'message', 
                       'created_at', 'updated_at')
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('user', 'name', 'email')
        }),
        ('Feedback Details', {
            'fields': ('subject', 'type', 'message')
        }),
        ('Status & Admin Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_in_progress', 'mark_resolved', 'mark_closed']
    
    def get_sender(self, obj):
        #Display sender name in list
        return obj.get_sender_display()
    get_sender.short_description = 'Sender'
    
    def mark_in_progress(self, request, queryset):
        count = queryset.update(status='IN_PROGRESS')
        self.message_user(request, f'{count} feedback marked as in progress.')
    mark_in_progress.short_description = 'Mark as in progress'
    
    def mark_resolved(self, request, queryset):
        count = queryset.update(status='RESOLVED')
        self.message_user(request, f'{count} feedback marked as resolved.')
    mark_resolved.short_description = 'Mark as resolved'
    
    def mark_closed(self, request, queryset):
        count = queryset.update(status='CLOSED')
        self.message_user(request, f'{count} feedback marked as closed.')
    mark_closed.short_description = 'Mark as closed'