// Main custom JavaScript for Job Search Tracker
// Add any custom JS here

document.addEventListener('DOMContentLoaded', function() {
    // Example: Dismiss alerts automatically after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.remove('show');
        }, 5000);
    });
});
