from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('position_title', 'company_name', 'user', 'status', 'application_date', 'created_at')
    list_filter = ('status', 'remote_option', 'application_date', 'created_at')
    search_fields = ('position_title', 'company_name', 'user__username', 'user__email')
    date_hierarchy = 'application_date'
    ordering = ('-application_date', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'company_name', 'position_title', 'application_date', 'status')
        }),
        ('Job Details', {
            'fields': ('job_description', 'job_url', 'salary_range', 'location', 'remote_option')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
