document.addEventListener('DOMContentLoaded', () => {

    /* ============ HAMBURGER MENU ============ */
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = navMenu.querySelectorAll('a');

    navToggle.addEventListener('click', () => {
        const isOpen = navMenu.classList.toggle('open');
        navToggle.classList.toggle('active');
        navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('open');
            navToggle.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        });
    });

    /* ============ FORM HANDLING ============ */
    const form = document.querySelector('.contacto form');
    const feedback = document.createElement('p');
    feedback.className = 'form-feedback';
    form.appendChild(feedback);

    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const submitBtn = form.querySelector('button');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Enviando...';

            feedback.textContent = '';
            feedback.className = 'form-feedback';

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'Accept': 'application/json' }
            })
            .then(response => {
                if (response.ok) {
                    feedback.textContent = '¡Mensaje enviado con éxito! Te contactaremos pronto.';
                    feedback.className = 'form-feedback form-feedback--success';
                    form.reset();
                } else {
                    throw new Error('Error al enviar');
                }
            })
            .catch(() => {
                feedback.textContent = 'Hubo un error al enviar el mensaje. Intenta de nuevo.';
                feedback.className = 'form-feedback form-feedback--error';
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Enviar';
            });
        });
    }

    /* ============ BACK TO TOP ============ */
    const backToTop = document.createElement('button');
    backToTop.className = 'back-to-top';
    backToTop.innerHTML = '&uarr;';
    backToTop.setAttribute('aria-label', 'Volver al inicio');
    document.body.appendChild(backToTop);

    window.addEventListener('scroll', () => {
        backToTop.classList.toggle('back-to-top--visible', window.scrollY > 400);
    }, { passive: true });

    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    /* ============ SMOOTH SCROLL NAV ============ */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                const offset = 70;
                const targetPos = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top: targetPos, behavior: 'smooth' });
            }
        });
    });
});
