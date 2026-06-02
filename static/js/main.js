// ========================================
// LOADING SCREEN
// ========================================
(function() {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const loading = document.getElementById('loading');
            if (loading) {
                loading.classList.remove('show');
            }
        }, 500);
    });
})();

// ========================================
// SCROLL EFFECT ON NAVBAR
// ========================================
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.85)';
        navbar.style.boxShadow = 'none';
    }
});

// ========================================
// CARD CLICK ANIMATION
// ========================================
document.querySelectorAll('.survey-card').forEach(card => {
    card.addEventListener('click', function(e) {
        if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                const link = this.querySelector('a');
                if (link) window.location.href = link.href;
                else window.location.href = this.dataset.href;
            }, 150);
        }
    });
});

// ========================================
// DROPDOWN CLOSE ON OUTSIDE CLICK
// ========================================
document.addEventListener('click', function(e) {
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        if (!dropdown.contains(e.target)) {
            const menu = dropdown.querySelector('.dropdown-menu');
            if (menu) {
                menu.style.opacity = '0';
                menu.style.visibility = 'hidden';
                menu.style.transform = 'translateY(-10px)';
            }
        }
    });
});