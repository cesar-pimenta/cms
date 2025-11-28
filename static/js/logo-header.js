/**
 * Logo Header Scroll Behavior Script
 * Hides/shows logo header on scroll, only on homepage
 * Smooth animations with requestAnimationFrame optimization
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        scrollThreshold: 80,  // pixels to scroll before hiding
        debounceDelay: 10      // ms for scroll debouncing
    };

    // Initialize when DOM is ready
    function init() {
        // Check if we're on the homepage
        const isHomepage = isOnHomepage();
        if (!isHomepage) {
            return;
        }

        // Get elements
        const logoHeader = document.getElementById('logo-header');
        const navbar = document.querySelector('.navbar');
        
        if (!logoHeader) {
            console.warn('Logo header element (#logo-header) not found');
            return;
        }

        // Mark page as homepage for CSS
        document.body.classList.add('page-home');

        // Setup scroll handler
        const scrollHandler = new ScrollHandler(logoHeader, navbar);
        
        // Listen for scroll events
        window.addEventListener('scroll', scrollHandler.onScroll.bind(scrollHandler), { 
            passive: true 
        });

        // Handle page visibility (mobile browsers)
        document.addEventListener('visibilitychange', function() {
            if (!document.hidden) {
                scrollHandler.update();
            }
        });

        console.log('Logo header scroll behavior initialized on homepage');
    }

    /**
     * Check if current page is the homepage
     */
    function isOnHomepage() {
        // Check for body class
        if (document.body.classList.contains('page-home')) {
            return true;
        }

        // Check for page-home ID
        if (document.body.id === 'page-home') {
            return true;
        }

        // Check URL path
        const path = window.location.pathname;
        if (path === '/' || path === '/portal/' || path === '/portal') {
            return true;
        }

        // Check for homepage marker in DOM
        if (document.querySelector('[data-page="home"]')) {
            return true;
        }

        return false;
    }

    /**
     * Scroll event handler with optimization
     */
    class ScrollHandler {
        constructor(logoHeader, navbar) {
            this.logoHeader = logoHeader;
            this.navbar = navbar;
            this.lastScrollY = 0;
            this.isHidden = false;
            this.ticking = false;
        }

        onScroll() {
            if (!this.ticking) {
                window.requestAnimationFrame(() => {
                    this.update();
                    this.ticking = false;
                });
                this.ticking = true;
            }
        }

        update() {
            const currentScrollY = window.pageYOffset || document.documentElement.scrollTop;
            
            // Determine if we should hide the header
            const shouldHide = currentScrollY > CONFIG.scrollThreshold && 
                              currentScrollY > this.lastScrollY;
            
            // Only update if state changed
            if (shouldHide && !this.isHidden) {
                this.hide();
                this.isHidden = true;
            } else if (!shouldHide && this.isHidden) {
                this.show();
                this.isHidden = false;
            }

            this.lastScrollY = currentScrollY;
        }

        hide() {
            this.logoHeader.classList.add('hide');
            if (this.navbar) {
                this.navbar.classList.add('navbar-hidden');
            }
        }

        show() {
            this.logoHeader.classList.remove('hide');
            if (this.navbar) {
                this.navbar.classList.remove('navbar-hidden');
            }
        }
    }

    // Initialize when DOM is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();

