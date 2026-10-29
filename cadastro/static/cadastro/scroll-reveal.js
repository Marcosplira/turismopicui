// Scroll Reveal Animation Library
(function() {
    'use strict';

    // Configuração padrão
    const defaultOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    // Classe para elementos que devem ser animados
    const revealClass = 'reveal-on-scroll';

    // Criar Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target); // Animar apenas uma vez
            }
        });
    }, defaultOptions);

    // Inicializar quando o DOM estiver pronto
    function init() {
        const elements = document.querySelectorAll(`.${revealClass}`);
        elements.forEach(el => {
            el.classList.add('reveal-hidden');
            observer.observe(el);
        });
    }

    // Inicializar imediatamente ou quando o DOM carregar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Tornar disponível globalmente
    window.ScrollReveal = {
        init: init,
        revealClass: revealClass
    };
})();
