from django.shortcuts import render
from django.http import HttpResponse
from apps.users.forms import ProfileUpdateForm
from apps.core.forms import JobApplicationForm
from django.contrib import messages


def home(request):
    """
    Home view that serves:
    - Landing page for unauthenticated users
    - Dashboard for authenticated users
    """
    if not request.user.is_authenticated:
        # Show landing page for unauthenticated users
        return render(request, 'home.html')
    
    # Dashboard logic for authenticated users
    profile_form = None
    job_application_form = None
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return render(request, 'home.html', get_dashboard_context(request, profile_form, job_application_form))
        elif 'add_job_application' in request.POST:
            job_application_form = JobApplicationForm(request.POST)
            if job_application_form.is_valid():
                job_application = job_application_form.save(commit=False)
                job_application.user = request.user
                job_application.save()
                messages.success(request, f'Job application for {job_application.position_title} at {job_application.company_name} has been added!')
                return render(request, 'home.html', get_dashboard_context(request, profile_form, job_application_form))
    
    # Initialize forms if not set by POST processing
    if profile_form is None:
        profile_form = ProfileUpdateForm(instance=request.user)
    if job_application_form is None:
        job_application_form = JobApplicationForm()
    
    return render(request, 'home.html', get_dashboard_context(request, profile_form, job_application_form))


def get_dashboard_context(request, profile_form, job_application_form):
    """Helper function to get dashboard context for authenticated users"""
    # Get user's job applications for dashboard stats
    job_applications = request.user.job_applications.all()
    stats = {
        'total_applications': job_applications.count(),
        'interviews_scheduled': job_applications.filter(status='interview_scheduled').count(),
        'offers_received': job_applications.filter(status='offer_received').count(),
        'under_review': job_applications.filter(status='under_review').count(),
    }
    
    return {
        'user': request.user,
        'profile_form': profile_form,
        'job_application_form': job_application_form,
        'job_applications': job_applications[:5],  # Recent 5 applications
        'stats': stats,
        'is_dashboard': True,  # Flag to indicate dashboard mode
    }
