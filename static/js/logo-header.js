// Logo Header Scroll Behavior - Homepage Only

document.addEventListener('DOMContentLoaded', function() {
    // Only execute on homepage
    const isHomepage = document.body.classList.contains('page-home') || 
                       document.body.id === 'page-home' ||
                       window.location.pathname === '/' ||
                       window.location.pathname === '/portal/';

    if (!isHomepage) {
        return;
    }

    const logoHeader = document.getElementById('logo-header');
    const mainContent = document.querySelector('main');
    
    if (!logoHeader) {
        console.warn('Logo header element not found');
        return;
    }

    let lastScrollY = 0;
    let isHeaderHidden = false;
    let scrollThreshold = 100; // Hide after scrolling 100px
    let ticking = false;

    function updateLogoHeaderPosition() {
        const currentScrollY = window.scrollY || window.pageYOffset;

        if (currentScrollY > scrollThreshold) {
            // Check scroll direction
            if (currentScrollY > lastScrollY) {
                // Scrolling DOWN - hide header
                if (!isHeaderHidden) {
                    logoHeader.classList.add('hide');
                    if (mainContent) {
                        mainContent.classList.add('logo-hidden');
                    }
                    isHeaderHidden = true;
                }
            } else {
                // Scrolling UP - show header
                if (isHeaderHidden) {
                    logoHeader.classList.remove('hide');
                    if (mainContent) {
                        mainContent.classList.remove('logo-hidden');
                    }
                    isHeaderHidden = false;
                }
            }
        } else {
            // At top - always show header
            if (isHeaderHidden) {
                logoHeader.classList.remove('hide');
                if (mainContent) {
                    mainContent.classList.remove('logo-hidden');
                }
                isHeaderHidden = false;
            }
        }

        lastScrollY = currentScrollY;
        ticking = false;
    }

    function onScroll() {
        if (!ticking) {
            window.requestAnimationFrame(updateLogoHeaderPosition);
            ticking = true;
        }
    }

    // Add scroll listener
    window.addEventListener('scroll', onScroll, { passive: true });

    // Initial state
    updateLogoHeaderPosition();

    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
        window.removeEventListener('scroll', onScroll);
    });

    console.log('Logo header scroll behavior initialized');
});
