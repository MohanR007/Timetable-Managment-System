// Handle page transitions
document.addEventListener('DOMContentLoaded', function() {
    // Add page transition class to main container
    document.querySelector('.container').classList.add('page-transition');

    // Add stagger animation to table rows
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach((row, index) => {
        row.classList.add('stagger-item');
        row.style.animationDelay = `${index * 0.1}s`;
    });

    // Add stagger animation to nav cards
    const navCards = document.querySelectorAll('.nav-card');
    navCards.forEach((card, index) => {
        card.classList.add('stagger-item');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Handle form submissions with loading animation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Show loading spinner
            submitButton.innerHTML = '<span class="loading-spinner"></span> Processing...';
            submitButton.disabled = true;

            // Simulate form submission (remove this in production)
            setTimeout(() => {
                submitButton.innerHTML = '✓ Success!';
                form.classList.add('form-success');
                
                // Reset button after animation
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 2000);
            }, 1000);
        });
    });

    // Handle navigation with smooth transitions
    const handleNavigation = (url, isBackButton = false) => {
        if (!isBackButton) {
            // Only push state if it's not a back button navigation
            history.pushState({ path: url }, '', url);
        }
        
        document.body.classList.add('page-exit');
        setTimeout(() => {
            window.location.href = url;
        }, 300);
    };

    // Handle clicks on navigation links
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!link.hasAttribute('data-no-transition') && !link.hasAttribute('target')) {
                e.preventDefault();
                const url = link.href;
                handleNavigation(url);
            }
        });
    });

    // Handle browser back button
    window.addEventListener('popstate', function(e) {
        if (e.state && e.state.path) {
            handleNavigation(e.state.path, true);
        } else {
            // If no state exists, just go back normally
            window.history.back();
        }
    });

    // Store initial state
    const initialPath = window.location.href;
    history.replaceState({ path: initialPath }, '', initialPath);

    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!button.classList.contains('no-ripple')) {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const ripple = document.createElement('span');
                ripple.style.left = `${x}px`;
                ripple.style.top = `${y}px`;
                ripple.classList.add('ripple');

                button.appendChild(ripple);
                setTimeout(() => ripple.remove(), 600);
            }
        });
    });

    // Add gradient text animation to headings
    document.querySelectorAll('.display-4, .display-5').forEach(heading => {
        heading.classList.add('gradient-text');
    });

    // Form input animation
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        input.addEventListener('focus', function() {
            this.closest('.mb-4').classList.add('input-focused');
        });

        input.addEventListener('blur', function() {
            this.closest('.mb-4').classList.remove('input-focused');
        });
    });
}); 