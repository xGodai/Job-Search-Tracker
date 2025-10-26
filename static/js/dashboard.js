document.addEventListener('DOMContentLoaded', function() {
    // 1) Set progress bar widths based on data-progress attributes
    const bars = document.querySelectorAll('.progress-bar[data-progress]');
    bars.forEach(function(bar) {
        const pct = parseInt(bar.getAttribute('data-progress') || '0', 10);
        if (!isNaN(pct)) {
            const clamped = Math.max(0, Math.min(100, pct));
            bar.style.width = clamped + '%';
            bar.setAttribute('aria-valuenow', String(clamped));
        }
    });

    // 2) Contact info toggle icon handling
    const contactInfo = document.getElementById('contactInfo');
    const toggleIcon = document.getElementById('contactToggleIcon');
    if (contactInfo && toggleIcon) {
        contactInfo.addEventListener('show.bs.collapse', function() {
            toggleIcon.classList.remove('fa-chevron-right');
            toggleIcon.classList.add('fa-chevron-down');
        });

        contactInfo.addEventListener('hide.bs.collapse', function() {
            toggleIcon.classList.remove('fa-chevron-down');
            toggleIcon.classList.add('fa-chevron-right');
        });
    }

    // 3) Auto-show profile/job application forms based on data flags
    const dashboardData = document.getElementById('dashboard-data');
    if (dashboardData) {
        const showProfile = dashboardData.getAttribute('data-show-profile') === '1';
        const showJobApp = dashboardData.getAttribute('data-show-jobapp') === '1';

        if (showProfile) {
            const el = document.getElementById('profileEditForm');
            if (el) {
                const c = new bootstrap.Collapse(el);
                c.show();
            }
        }

        if (showJobApp) {
            const el = document.getElementById('jobApplicationForm');
            if (el) {
                const c = new bootstrap.Collapse(el);
                c.show();
            }
        }
    }
});
