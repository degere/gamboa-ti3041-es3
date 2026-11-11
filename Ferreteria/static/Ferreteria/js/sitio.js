// McHammer · comportamiento de los carruseles (sin librerías externas)
(function () {
    'use strict';

    // ---- Carrusel principal (banner con diapositivas) ----
    document.querySelectorAll('[data-hero]').forEach(function (hero) {
        var slides = hero.querySelectorAll('.hero-slide');
        var dots = hero.querySelectorAll('.hero-dot');
        var actual = 0;
        var timer = null;
        if (slides.length < 2) { return; }

        function mostrar(i) {
            actual = (i + slides.length) % slides.length;
            slides.forEach(function (s, n) {
                s.classList.toggle('is-active', n === actual);
                s.setAttribute('aria-hidden', n === actual ? 'false' : 'true');
            });
            dots.forEach(function (d, n) { d.classList.toggle('is-active', n === actual); });
        }

        function detener() {
            if (timer) { clearInterval(timer); timer = null; }
        }

        function iniciar() {
            detener();
            timer = setInterval(function () { mostrar(actual + 1); }, 4000);
        }

        hero.querySelector('.hero-btn.prev').addEventListener('click', function () { mostrar(actual - 1); iniciar(); });
        hero.querySelector('.hero-btn.next').addEventListener('click', function () { mostrar(actual + 1); iniciar(); });
        dots.forEach(function (d, n) {
            d.addEventListener('click', function () { mostrar(n); iniciar(); });
        });

        hero.addEventListener('mouseenter', detener);
        hero.addEventListener('mouseleave', iniciar);
        hero.addEventListener('focusin', detener);
        hero.addEventListener('focusout', iniciar);

        mostrar(0);
        iniciar();
    });

    // ---- Carruseles de productos (autoplay + loop, con botones manuales) ----
    document.querySelectorAll('[data-carrusel]').forEach(function (carrusel) {
        var pista = carrusel.querySelector('.carrusel-pista');
        if (!pista) { return; }
        var timer = null;

        function detener() {
            if (timer) { clearInterval(timer); timer = null; }
        }

        function iniciar() {
            detener();
            timer = setInterval(function () {
                // Si llegó al final, vuelve suavemente al primer elemento
                var llegoAlFinal = pista.scrollLeft + pista.clientWidth >= pista.scrollWidth - 1;
                if (llegoAlFinal) {
                    pista.scrollTo({ left: 0, behavior: 'smooth' });
                } else {
                    pista.scrollBy({ left: pista.clientWidth * 0.8, behavior: 'smooth' });
                }
            }, 4000);
        }

        carrusel.querySelectorAll('.carrusel-btn').forEach(function (boton) {
            boton.addEventListener('click', function () {
                var direccion = boton.classList.contains('next') ? 1 : -1;
                pista.scrollBy({ left: direccion * pista.clientWidth * 0.8, behavior: 'smooth' });
            });
        });

        // Pausa el autoplay mientras el usuario interactúa con el carrusel
        carrusel.addEventListener('mouseenter', detener);
        carrusel.addEventListener('mouseleave', iniciar);

        iniciar();
    });
})();
