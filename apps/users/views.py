from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from apps.core.forms import JobApplicationForm


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Support next parameter from POST (hidden input) or GET with safety check
                raw_next = request.POST.get('next') or request.GET.get('next')
                if raw_next and url_has_allowed_host_and_scheme(raw_next, allowed_hosts={request.get_host()}):
                    return redirect(raw_next)
                return redirect('users:dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard_view(request):
    """User dashboard view with embedded profile editing and job application form"""
    profile_form = None
    job_application_form = None
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('users:dashboard')
        elif 'add_job_application' in request.POST:
            job_application_form = JobApplicationForm(request.POST)
            if job_application_form.is_valid():
                job_application = job_application_form.save(commit=False)
                job_application.user = request.user
                job_application.save()
                messages.success(request, f'Job application for {job_application.position_title} at {job_application.company_name} has been added!')
                return redirect('users:dashboard')
    
    # Initialize forms if not set by POST processing
    if profile_form is None:
        profile_form = ProfileUpdateForm(instance=request.user)
    if job_application_form is None:
        job_application_form = JobApplicationForm()
    
    # Get user's job applications for dashboard stats
    job_applications = request.user.job_applications.all()
    stats = {
        'total_applications': job_applications.count(),
        'interviews_scheduled': job_applications.filter(status='interview_scheduled').count(),
        'offers_received': job_applications.filter(status='offer_received').count(),
        'under_review': job_applications.filter(status='under_review').count(),
    }
    
    return render(request, 'users/dashboard.html', {
        'user': request.user,
        'profile_form': profile_form,
        'job_application_form': job_application_form,
        'job_applications': job_applications[:5],  # Recent 5 applications
        'stats': stats,
    })


@login_required
def profile_view(request):
    """Redirect to dashboard since profile editing is now embedded there"""
    return redirect('users:dashboard')