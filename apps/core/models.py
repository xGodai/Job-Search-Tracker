from django.db import models
from django.conf import settings


class JobApplication(models.Model):
    """Model representing a job application"""
    
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_completed', 'Interview Completed'),
        ('offer_received', 'Offer Received'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    # Basic Information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    company_name = models.CharField(max_length=200)
    position_title = models.CharField(max_length=200)
    job_description = models.TextField(blank=True)
    
    # Application Details
    application_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    job_url = models.URLField(blank=True, help_text="Link to the job posting")
    
    # Contact Information
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Additional Information
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., $50,000 - $70,000")
    location = models.CharField(max_length=200, blank=True)
    remote_option = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-application_date', '-created_at']
        
    def __str__(self):
        return f"{self.position_title} at {self.company_name}"
