document.addEventListener('DOMContentLoaded', () => {

    /* ============ CATALOGO ============ */
    const PAGE_SIZE = 12;
    const PAGINAS = {};

    const catalogoGrid = document.getElementById('catalogoGrid');
    const tabs = document.querySelectorAll('.tab-btn');
    let categoriaActiva = 'todas';
    let busquedaActiva = '';

    let paginacionContainer = document.getElementById('paginacion');

    function renderizarPaginacion(total, paginaActual) {
        const totalPages = Math.ceil(total / PAGE_SIZE);
        if (totalPages <= 1) {
            paginacionContainer.innerHTML = '';
            return;
        }
        let html = '';
        for (let i = 1; i <= totalPages; i++) {
            html += `<button class="page-btn ${i === paginaActual ? 'active' : ''}" data-page="${i}">${i}</button>`;
        }
        paginacionContainer.innerHTML = html;
    }

    function renderizarProductos(categoria) {
        const porCategoria = categoria === 'todas'
            ? productos
            : productos.filter(p => p.categoria === categoria);
        const filtrados = busquedaActiva
            ? porCategoria.filter(p => p.nombre.toLowerCase().includes(busquedaActiva))
            : porCategoria;

        if (filtrados.length === 0) {
            catalogoGrid.innerHTML = '<p style="grid-column:1/-1;text-align:center;color:#888;padding:40px 0;">No hay productos en esta categoría.</p>';
            paginacionContainer.innerHTML = '';
            return;
        }

        const paginaActual = PAGINAS[categoria] || 1;
        const totalPages = Math.ceil(filtrados.length / PAGE_SIZE);
        const start = (paginaActual - 1) * PAGE_SIZE;
        const visibles = filtrados.slice(start, start + PAGE_SIZE);

        catalogoGrid.innerHTML = visibles.map(p => `
            <div class="producto-card">
                <img src="${p.imagen}" alt="${p.nombre}" loading="lazy">
                <div class="producto-info">
                    <span class="producto-categoria">${p.categoria}</span>
                    <h4>${p.nombre}</h4>
                    <span class="producto-precio">$${p.precio}</span>
                    <span class="producto-tallas">Tallas: ${p.tallas.join(', ')}</span>
                    <button class="btn-add-cart" data-id="${p.id}">Añadir al carrito</button>
                </div>
            </div>
        `).join('');

        renderizarPaginacion(filtrados.length, paginaActual);
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            categoriaActiva = tab.dataset.categoria;
            PAGINAS[categoriaActiva] = 1;
            renderizarProductos(categoriaActiva);
        });
    });

    paginacionContainer.addEventListener('click', (e) => {
        const btn = e.target.closest('.page-btn');
        if (!btn) return;
        const page = parseInt(btn.dataset.page);
        PAGINAS[categoriaActiva] = page;
        renderizarProductos(categoriaActiva);
    });

    const searchInput = document.getElementById('catalogoSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            busquedaActiva = e.target.value.toLowerCase().trim();
            PAGINAS[categoriaActiva] = 1;
            renderizarProductos(categoriaActiva);
        });
    }

    async function cargarProductos() {
        try {
            const res = await fetch(`${API_URL}/api/products`);
            if (res.ok) {
                const apiProducts = await res.json();
                if (Array.isArray(apiProducts) && apiProducts.length > 0) {
                    window.productos = apiProducts;
                }
            }
        } catch {}
        mostrarSkeletonCatalog();
        setTimeout(() => {
            PAGINAS['todas'] = 1;
            renderizarProductos('todas');
        }, 300);
    }
    cargarProductos();

    /* ============ EVENT DELEGATION: ADD TO CART ============ */
    let productoSeleccionado = null;

    catalogoGrid.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-add-cart');
        if (!btn) return;
        const id = parseInt(btn.dataset.id);
        productoSeleccionado = productos.find(p => p.id === id);
        if (!productoSeleccionado) return;
        abrirModal(productoSeleccionado);
    });

    /* ============ CART ============ */
    let cart = JSON.parse(localStorage.getItem('suarezCart') || '[]');

    function guardarCart() {
        localStorage.setItem('suarezCart', JSON.stringify(cart));
    }

    function actualizarContador() {
        const count = cart.reduce((sum, item) => sum + item.cantidad, 0);
        document.getElementById('cartCount').textContent = count;
    }

    function calcularTotal() {
        return cart.reduce((sum, item) => sum + item.precio * item.cantidad, 0);
    }

    function renderizarCart() {
        const body = document.getElementById('cartDrawerBody');
        const footer = document.getElementById('cartDrawerFooter');
        const totalEl = document.getElementById('cartTotal');
        const checkoutBtn = document.getElementById('btnCheckout');

        if (cart.length === 0) {
            body.innerHTML = '<p class="cart-empty">Tu carrito está vacío</p>';
            totalEl.textContent = '$0';
            checkoutBtn.disabled = true;
            return;
        }

        body.innerHTML = cart.map((item, index) => `
            <div class="cart-item">
                <img src="${item.imagen}" alt="${item.nombre}" loading="lazy">
                <div class="cart-item-info">
                    <h4>${item.nombre}</h4>
                    <span class="cart-item-detalle">${item.talla} / ${item.color}</span>
                    <span class="cart-item-precio">$${item.precio}</span>
                    <div class="cart-item-actions">
                        <button class="cart-item-minus" data-index="${index}">−</button>
                        <span class="cart-item-cantidad">${item.cantidad}</span>
                        <button class="cart-item-plus" data-index="${index}">+</button>
                        <button class="cart-item-remove" data-index="${index}">Eliminar</button>
                    </div>
                </div>
            </div>
        `).join('');

        totalEl.textContent = `$${calcularTotal()}`;
        checkoutBtn.disabled = false;
    }

    function agregarAlCarrito(producto, talla, color) {
        const existente = cart.findIndex(
            item => item.id === producto.id && item.talla === talla && item.color === color
        );
        if (existente > -1) {
            cart[existente].cantidad += 1;
        } else {
            cart.push({
                id: producto.id,
                nombre: producto.nombre,
                precio: producto.precio,
                imagen: producto.imagen,
                talla: talla,
                color: color,
                cantidad: 1
            });
        }
        guardarCart();
        actualizarContador();
        renderizarCart();
    }

    function eliminarDelCarrito(index) {
        cart.splice(index, 1);
        guardarCart();
        actualizarContador();
        renderizarCart();
    }

    function cambiarCantidad(index, delta) {
        const nueva = cart[index].cantidad + delta;
        if (nueva <= 0) {
            eliminarDelCarrito(index);
            return;
        }
        cart[index].cantidad = nueva;
        guardarCart();
        actualizarContador();
        renderizarCart();
    }

    /* ============ MODAL ============ */
    const modalOverlay = document.getElementById('modalOverlay');
    const modal = document.getElementById('modalProducto');
    const modalClose = document.getElementById('modalClose');
    const modalNombre = document.getElementById('modalProductoNombre');
    const modalImg = document.getElementById('modalProductoImg');
    const modalTalla = document.getElementById('modalTalla');
    const modalColor = document.getElementById('modalColor');
    const btnConfirmar = document.getElementById('btnConfirmarCarrito');

    function abrirModal(producto) {
        modalNombre.textContent = producto.nombre;
        modalImg.src = producto.imagen;
        modalImg.alt = producto.nombre;

        modalTalla.innerHTML = producto.tallas.map(t => `<option value="${t}">${t}</option>`).join('');
        modalColor.innerHTML = producto.colores.map(c => `<option value="${c}">${c}</option>`).join('');

        modalOverlay.classList.add('open');
        modal.classList.add('open');
    }

    function cerrarModal() {
        modalOverlay.classList.remove('open');
        modal.classList.remove('open');
        productoSeleccionado = null;
    }

    modalClose.addEventListener('click', cerrarModal);
    modalOverlay.addEventListener('click', cerrarModal);

    btnConfirmar.addEventListener('click', () => {
        if (!productoSeleccionado) return;
        const talla = modalTalla.value;
        const color = modalColor.value;
        agregarAlCarrito(productoSeleccionado, talla, color);
        cerrarModal();
        abrirDrawer();
    });

    /* ============ DRAWER ============ */
    const cartBtn = document.getElementById('cartBtn');
    const cartDrawer = document.getElementById('cartDrawer');
    const cartOverlay = document.getElementById('cartOverlay');
    const cartDrawerClose = document.getElementById('cartDrawerClose');

    function abrirDrawer() {
        cartDrawer.classList.add('open');
        cartOverlay.classList.add('open');
        renderizarCart();
    }

    function cerrarDrawer() {
        cartDrawer.classList.remove('open');
        cartOverlay.classList.remove('open');
        mostrarCarrito();
        resetCheckout();
        renderizarCart();
    }

    cartBtn.addEventListener('click', abrirDrawer);
    cartDrawerClose.addEventListener('click', cerrarDrawer);
    cartOverlay.addEventListener('click', cerrarDrawer);

    /* ============ DRAWER EVENT DELEGATION ============ */
    document.getElementById('cartDrawerBody').addEventListener('click', (e) => {
        const btn = e.target;
        if (btn.classList.contains('cart-item-plus')) {
            cambiarCantidad(parseInt(btn.dataset.index), 1);
        } else if (btn.classList.contains('cart-item-minus')) {
            cambiarCantidad(parseInt(btn.dataset.index), -1);
        } else if (btn.classList.contains('cart-item-remove')) {
            eliminarDelCarrito(parseInt(btn.dataset.index));
        }
    });

    /* ============ CHECKOUT VIEW ============ */
    const cartView = document.getElementById('cartView');
    const checkoutView = document.getElementById('checkoutView');
    const checkoutResumen = document.getElementById('checkoutResumen');
    const checkoutForm = document.getElementById('checkoutForm');
    const cartDrawerBack = document.getElementById('cartDrawerBack');
    const cartDrawerTitle = document.getElementById('cartDrawerTitle');
    const btnEnviarPedido = document.getElementById('btnEnviarPedido');

    function mostrarCheckout() {
        if (cart.length === 0) return;
        cartView.classList.add('hidden');
        checkoutView.classList.remove('hidden');
        cartDrawerBack.classList.add('visible');
        cartDrawerTitle.textContent = 'Finalizar pedido';

        checkoutResumen.innerHTML = `
            <h4>Resumen del pedido</h4>
            ${cart.map(item => `
                <div class="checkout-resumen-item">
                    <span class="checkout-item-nombre">${item.nombre}</span>
                    <span class="checkout-item-cant">${item.talla} / ${item.color} x${item.cantidad}</span>
                    <span class="checkout-item-precio">$${item.precio * item.cantidad}</span>
                </div>
            `).join('')}
            <div class="checkout-resumen-total">
                <span>Total</span>
                <span>$${calcularTotal()}</span>
            </div>
        `;
    }

    function mostrarCarrito() {
        cartView.classList.remove('hidden');
        checkoutView.classList.add('hidden');
        cartDrawerBack.classList.remove('visible');
        cartDrawerTitle.textContent = 'Carrito';
    }

    document.getElementById('btnCheckout').addEventListener('click', mostrarCheckout);
    cartDrawerBack.addEventListener('click', mostrarCarrito);

    checkoutForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (cart.length === 0) return;

        const nombre = document.getElementById('checkoutNombre').value.trim();
        const telefono = document.getElementById('checkoutTelefono').value.trim();
        const direccion = document.getElementById('checkoutDireccion').value.trim();
        const notas = document.getElementById('checkoutNotas').value.trim();

        if (!nombre || !telefono || !direccion) return;

        btnEnviarPedido.disabled = true;
        btnEnviarPedido.textContent = 'Enviando...';

        const items = cart.map(item => ({
            nombre: item.nombre,
            talla: item.talla,
            color: item.color,
            cantidad: item.cantidad,
            precio: item.precio,
        }));

        const total = calcularTotal();

        const pedidoData = {
            customer_name: nombre,
            phone: telefono,
            address: direccion,
            items: items,
            total: total,
            notes: notas,
        };

        fetch(`${API_URL}/api/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pedidoData),
        }).catch(() => {});

        const itemsWhatsApp = cart.map(item =>
            `• ${item.nombre} (${item.talla} / ${item.color}) x${item.cantidad} — $${item.precio * item.cantidad}`
        ).join('%0A');

        const msjNotas = notas ? `%0A%0ANotas: ${notas}` : '';
        const mensaje = `¡Hola! Quiero hacer un pedido:%0A%0A${itemsWhatsApp}%0A%0ATotal: $${total}%0A%0ADatos del cliente:%0ANombre: ${nombre}%0ATeléfono: ${telefono}%0ADirección: ${direccion}${msjNotas}`;

        window.open(`https://wa.me/584148287893?text=${mensaje}`, '_blank');

        checkoutForm.reset();
        cart.length = 0;
        guardarCart();
        actualizarContador();

        checkoutResumen.innerHTML = `
            <div class="checkout-confirmacion visible">
                <div class="check-icon">✓</div>
                <h3>¡Pedido enviado!</h3>
                <p>Tu pedido se ha enviado por WhatsApp. Te contactaremos pronto para confirmar.</p>
            </div>
        `;
        checkoutForm.style.display = 'none';
        btnEnviarPedido.textContent = 'Pedido enviado';
    });

    function resetCheckout() {
        checkoutForm.style.display = 'flex';
        checkoutForm.reset();
        btnEnviarPedido.disabled = false;
        btnEnviarPedido.textContent = 'Enviar pedido por WhatsApp';
    }

    /* ============ INIT CART ============ */
    actualizarContador();

    /* ============ TESTIMONIOS CARRUSEL ============ */
    let testimoniosData = [];
    let testimonioIndex = 0;
    let testimonioInterval = null;
    const track = document.getElementById('testimoniosTrack');
    const dotsContainer = document.getElementById('testimoniosDots');
    const prevBtn = document.getElementById('testimonioPrev');
    const nextBtn = document.getElementById('testimonioNext');

    function renderTestimonio(index) {
        const t = testimoniosData[index];
        if (!t) return;
        const estrellas = '★'.repeat(t.rating || t.valoracion || 5) + '☆'.repeat(5 - (t.rating || t.valoracion || 5));
        const ciudad = t.ciudad ? `${t.ciudad}, ` : '';
        track.innerHTML = `
            <div class="testimonio-card">
                <div class="testimonio-estrellas">${estrellas}</div>
                <p class="testimonio-texto">${t.opinion}</p>
                <div class="testimonio-autor">
                    <span class="testimonio-nombre">— ${t.name || t.nombre}</span>
                    <span class="testimonio-ciudad">${ciudad}${t.product || t.producto}</span>
                </div>
            </div>
        `;
        dotsContainer.querySelectorAll('.dot').forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }

    function goTestimonio(index) {
        testimonioIndex = index;
        renderTestimonio(testimonioIndex);
        reiniciarAutoPlay();
    }

    function nextTestimonio() {
        goTestimonio((testimonioIndex + 1) % testimoniosData.length);
    }

    function prevTestimonio() {
        goTestimonio((testimonioIndex - 1 + testimoniosData.length) % testimoniosData.length);
    }

    function reiniciarAutoPlay() {
        clearInterval(testimonioInterval);
        testimonioInterval = setInterval(nextTestimonio, 5000);
    }

    async function cargarTestimonios() {
        track.innerHTML = `
            <div class="testimonio-card">
                <div class="skeleton" style="width:120px;height:28px;margin:0 auto 20px;border-radius:4px;"></div>
                <div class="skeleton" style="width:80%;height:80px;margin:0 auto 25px;border-radius:8px;"></div>
                <div class="skeleton" style="width:150px;height:16px;margin:0 auto;border-radius:4px;"></div>
            </div>
        `;
        try {
            const res = await fetch(`${API_URL}/api/testimonials`);
            if (res.ok) {
                testimoniosData = await res.json();
            } else {
                throw new Error('API not available');
            }
        } catch {
            try {
                const res = await fetch('docs/opiniones.json');
                const data = await res.json();
                testimoniosData = (data.testimonios || []).map(t => ({
                    name: t.nombre,
                    product: t.producto,
                    opinion: t.opinion,
                    rating: t.valoracion,
                    ciudad: t.ciudad || '',
                }));
            } catch {
                testimoniosData = [];
            }
        }

        if (testimoniosData.length === 0) {
            track.innerHTML = `
                <div class="testimonio-card">
                    <div class="testimonio-estrellas">★★★★★</div>
                    <p class="testimonio-texto">"No hay testimonios disponibles en este momento."</p>
                    <div class="testimonio-autor">
                        <span class="testimonio-nombre">— Suarez Sport</span>
                    </div>
                </div>
            `;
            return;
        }

        dotsContainer.innerHTML = testimoniosData.map((_, i) =>
            `<button class="dot ${i === 0 ? 'active' : ''}" data-index="${i}" aria-label="Testimonio ${i + 1}"></button>`
        ).join('');

        dotsContainer.addEventListener('click', (e) => {
            const dot = e.target.closest('.dot');
            if (dot) goTestimonio(parseInt(dot.dataset.index));
        });

        renderTestimonio(0);
        reiniciarAutoPlay();
    }

    prevBtn.addEventListener('click', prevTestimonio);
    nextBtn.addEventListener('click', nextTestimonio);

    const testimoniosSection = document.getElementById('testimonios');
    testimoniosSection.addEventListener('mouseenter', () => clearInterval(testimonioInterval));
    testimoniosSection.addEventListener('mouseleave', reiniciarAutoPlay);

    cargarTestimonios();

    /* ============ INTERSECTION OBSERVER ============ */
    const animados = document.querySelectorAll('.animate-on-scroll');
    if (animados.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });
        animados.forEach(el => observer.observe(el));
    }

    /* ============ SKELETON LOADERS ============ */
    function mostrarSkeletonCatalog() {
        const grid = document.getElementById('catalogoGrid');
        grid.innerHTML = Array(6).fill(0).map(() => `
            <div class="skeleton-card">
                <div class="skeleton skeleton-img"></div>
                <div class="skeleton-body">
                    <div class="skeleton skeleton-line short"></div>
                    <div class="skeleton skeleton-line medium"></div>
                    <div class="skeleton skeleton-line short"></div>
                </div>
            </div>
        `).join('');
    }

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

            const nombre = document.getElementById('nombre')?.value || form.querySelector('[name="nombre"]')?.value || '';
            const email = document.getElementById('email')?.value || form.querySelector('[name="email"]')?.value || '';
            const mensaje = document.getElementById('mensaje')?.value || form.querySelector('[name="mensaje"]')?.value || '';

            const apiPromise = fetch(`${API_URL}/api/contact`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: nombre, email, message: mensaje }),
            }).catch(() => {});

            const fallbackPromise = fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: { 'Accept': 'application/json' },
            }).catch(() => {});

            Promise.allSettled([apiPromise, fallbackPromise]).then(() => {
                feedback.textContent = '¡Mensaje enviado con éxito! Te contactaremos pronto.';
                feedback.className = 'form-feedback form-feedback--success';
                form.reset();
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
