from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    """Form for creating and updating job applications"""
    
    class Meta:
        model = JobApplication
        fields = [
            'company_name', 'position_title', 'job_description', 'application_date',
            'status', 'job_url', 'contact_person', 'contact_email', 'contact_phone',
            'salary_range', 'location', 'remote_option', 'notes'
        ]
        widgets = {
            'application_date': forms.DateInput(attrs={'type': 'date'}),
            'job_description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
        
        # Set placeholders for better UX
        self.fields['company_name'].widget.attrs['placeholder'] = 'e.g., Google, Microsoft, Startup Inc.'
        self.fields['position_title'].widget.attrs['placeholder'] = 'e.g., Software Engineer, Data Scientist'
        self.fields['job_url'].widget.attrs['placeholder'] = 'https://...'
        self.fields['contact_person'].widget.attrs['placeholder'] = 'e.g., John Smith (HR Manager)'
        self.fields['contact_email'].widget.attrs['placeholder'] = 'recruiter@company.com'
        self.fields['contact_phone'].widget.attrs['placeholder'] = '+1 (555) 123-4567'
        self.fields['salary_range'].widget.attrs['placeholder'] = 'e.g., $50,000 - $70,000'
        self.fields['location'].widget.attrs['placeholder'] = 'e.g., New York, NY or Remote'
        self.fields['notes'].widget.attrs['placeholder'] = 'Any additional notes or thoughts about this application...'
        # Allow the view to default application_date if user leaves it blank.
        # The model requires application_date, but making the form field optional
        # lets us set a sensible default (today) server-side before saving.
        if 'application_date' in self.fields:
            self.fields['application_date'].required = False