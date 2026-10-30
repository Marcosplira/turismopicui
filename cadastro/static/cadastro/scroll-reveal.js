// Scroll Reveal Animation Library para Turismo de Picuí
(function() {
    'use strict';

    // Injeta o CSS essencial automaticamente para animações fluidas
    if (!document.getElementById('scroll-reveal-styles')) {
        const style = document.createElement('style');
        style.id = 'scroll-reveal-styles';
        style.textContent = `
            .reveal-on-scroll {
                opacity: 0;
                transform: translateY(24px);
                transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
                will-change: opacity, transform;
            }
            .reveal-on-scroll.revealed {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
            .reveal-stagger-1 { transition-delay: 80ms; }
            .reveal-stagger-2 { transition-delay: 160ms; }
            .reveal-stagger-3 { transition-delay: 240ms; }
            .reveal-stagger-4 { transition-delay: 320ms; }
            .reveal-stagger-5 { transition-delay: 400ms; }
        `;
        document.head.appendChild(style);
    }

    const defaultOptions = {
        threshold: 0.08,
        rootMargin: '0px 0px -40px 0px'
    };

    const revealClass = 'reveal-on-scroll';

    if (!('IntersectionObserver' in window)) {
        document.querySelectorAll(`.${revealClass}`).forEach(el => el.classList.add('revealed'));
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, defaultOptions);

    function init() {
        const elements = document.querySelectorAll(`.${revealClass}`);
        elements.forEach(el => {
            observer.observe(el);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    window.ScrollReveal = {
        init: init,
        revealClass: revealClass
    };
})();
