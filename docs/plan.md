# Plan de Ejecución — Suarez Sport Web Completa

## Plan de Ejecución — Frontend (suarezsport.github.io)

### Fase 1: Catálogo dinámico
- [ ] Crear `js/productos.js` con array de productos (nombre, categoría, precio, imágenes, tallas, colores)
- [ ] Agregar sección `<section id="catalogo">` al `index.html` con tabs de categorías y grid de tarjetas
- [ ] CSS: grid responsive, tarjetas dark-theme coherentes, tabs de categorías
- [ ] JS: renderizar productos, filtrar por categoría, preparar estructura para API futura
- [ ] Agregar "Catálogo" al menú de navegación

### Fase 2: Carrito de compras
- [x] Icono de carrito en header con contador
- [x] Drawer lateral con lista de items del carrito
- [x] Botones "Añadir al carrito" en tarjetas con selector de talla/color
- [x] Persistencia en localStorage
- [x] Actualizar contador en tiempo real

### Fase 3: Checkout
- [x] Botón "Finalizar pedido" → vista de checkout dentro del drawer
- [x] Formulario: resumen del pedido → datos cliente (nombre, teléfono, dirección) → notas
- [x] Al enviar: abre WhatsApp con todos los datos + resumen + datos de envío
- [x] Confirmación visual + carrito se vacía automáticamente

### Fase 4: Testimonios dinámicos
- [x] Carrusel de testimonios cargado desde `docs/opiniones.json` (fallback local)
- [x] Preparado para consumir `GET /api/testimonials` cuando exista backend (cambiar fetch)
- [x] Navegación: botones prev/next + dots + auto-rotación 5s + pausa en hover
- [x] Diseño responsive

### Fase 5: UX y animaciones
- [x] Intersection Observer para fade-in/slide-up en todas las secciones
- [x] Lazy loading de imágenes (nativo + en tarjetas de productos)
- [x] Skeleton loaders para catálogo y testimonios
- [x] Estados de error amigables (testimonios fallback, carrito vacío, etc.)
- [x] Animaciones con delays escalonados para cards y FAQ

### Fase 6: SEO y rendimiento
- [x] Meta tags: description, keywords, OG (title, description, image, url, type, locale), Twitter Cards
- [x] JSON-LD structured data (Store schema con dirección, contacto, redes sociales)
- [x] Sitemap básico (`sitemap.xml`)
- [x] `robots.txt`
- [x] Canonical URL, preconnect hints
- [x] Optimización de imágenes: JPEG → WebP (personalizacion, variedad)
- [x] Alt text descriptivos en todas las imágenes

### Fase 7: Backend (monorepo — backend/)
- [x] Estructura del proyecto: `backend/` con FastAPI + routers + admin
- [x] Modelos SQLAlchemy: Product, Order, Testimonial, ContactMessage, User
- [x] Schemas Pydantic
- [x] Auth JWT con cookies
- [x] API pública: `GET /api/products`, `GET /api/categories`, `GET /api/testimonials`, `POST /api/orders`, `POST /api/contact`
- [x] Admin panel Jinja2: login, dashboard, CRUD productos, pedidos (cambiar estado), testimonios (aprobar/ocultar), mensajes
- [x] Cloudinary utils (subir/borrar imágenes)
- [x] Dockerfile para deploy en Render
- [x] Crear cuenta Supabase, proyecto y bucket `productos`
- [x] `storage_utils.py` con Supabase Storage (subir/borrar imágenes)
- [ ] **Pendiente deploy en Render**: conectar repo, configurar variables de entorno
- [ ] **Pendiente**: Crear usuario admin (`python -m app.create_admin admin <pass>`)
- [ ] **Pendiente**: Migrar datos locales (productos.js) a la BD
- [ ] **Pendiente**: Conectar frontend a la API real

---

## Arquitectura

```
suarezsport.github.io/   → Frontend (HTML/CSS/JS)   → Vercel
suarezsport-backend/     → Backend (FastAPI + PostgreSQL) → Render / Railway
```

---

## Backend — FastAPI + PostgreSQL

### Estructura del proyecto

```
suarezsport-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app, CORS, montado de routers
│   ├── config.py              # Variables de entorno (DB URL, SECRET_KEY, etc.)
│   ├── database.py            # SQLAlchemy engine + sesión
│   ├── models.py              # Modelos SQLAlchemy
│   ├── schemas.py             # Pydantic schemas
│   ├── dependencies.py        # Dependencias (auth, get_db)
│   ├── auth.py                # JWT login, hash de contraseñas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── products.py        # CRUD productos (público)
│   │   ├── orders.py          # Crear/consultar pedidos
│   │   ├── testimonials.py    # Testimonios activos (público)
│   │   └── contact.py         # Formulario de contacto
│   └── admin/
│       ├── __init__.py
│       ├── router.py          # CRUD protegido (productos, pedidos, testimonios)
│       ├── templates/         # Jinja2 templates
│       │   ├── base.html
│       │   ├── login.html
│       │   ├── dashboard.html
│       │   ├── products.html
│       │   ├── product_form.html
│       │   ├── orders.html
│       │   └── testimonials.html
│       └── static/            # CSS/JS para admin
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

### Modelos de base de datos

| Tabla | Columnas |
|-------|----------|
| **User** | id, username, hashed_password, is_admin |
| **Product** | id, name, description, category, price, images (JSON), sizes (JSON), colors (JSON), created_at, updated_at |
| **Order** | id, customer_name, phone, address, items (JSON), total, status (enum), notes, created_at |
| **Testimonial** | id, name, product, opinion, rating, active (bool), created_at |
| **ContactMessage** | id, name, email, message, created_at, read (bool) |

### API endpoints

#### Públicos (consume el frontend)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/products` | Listar productos (filtro: ?category=, ?search=) |
| GET | `/api/products/{id}` | Detalle de producto |
| GET | `/api/categories` | Listar categorías disponibles |
| POST | `/api/orders` | Crear pedido |
| GET | `/api/testimonials` | Testimonios activos |
| POST | `/api/contact` | Enviar mensaje de contacto |

#### Admin (protegido con JWT + sesión)

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/admin/api/login` | Iniciar sesión |
| GET | `/admin/dashboard` | Dashboard con stats |
| CRUD | `/admin/products[/{id}]` | Gestión de productos |
| GET/PATCH | `/admin/orders/{id}` | Ver/actualizar pedido |
| CRUD | `/admin/testimonials[/{id}]` | Gestión de testimonios |
| GET/PATCH | `/admin/messages[/{id}]` | Ver mensajes de contacto |

### Fases de implementación

#### Fase 1: Proyecto base
- Crear estructura del proyecto
- Configurar FastAPI + SQLAlchemy + PostgreSQL
- Definir modelos y migraciones (Alembic)
- Configurar CORS

#### Fase 2: API pública
- Router de productos (CRUD básico)
- Router de testimonios (solo activos)
- Router de pedidos (crear y listar)
- Router de contacto

#### Fase 3: Auth + Admin panel
- Sistema de autenticación JWT
- Dashboard admin con Jinja2
- CRUD de productos desde admin
- Gestión de pedidos (cambiar estado)
- Gestión de testimonios (aprobar/ocultar)
- Ver mensajes de contacto

#### Fase 4: Deploy
- Dockerfile para Render/Railway
- Variables de entorno
- Migraciones automáticas al iniciar
- Pruebas de integración

---

## Frontend — HTML/CSS/JS (Vercel)

### Estructura actual (se mantiene)

```
suarezsport.github.io/
├── index.html
├── css/index.css
├── js/script.js
├── imagenes/
│   ├── uniformes/
│   ├── sueter/
│   ├── short/
│   ├── camisas/
│   ├── conjuntos/
│   ├── accesorios/
│   ├── presentacion/
│   ├── clientes/
│   └── logos...
└── docs/
    ├── opiniones.json
    └── plan.md
```

### Fases de implementación

#### Fase 5: Catálogo dinámico
- Agregar sección de productos por categorías (camisas, shorts, conjuntos, suéteres, accesorios, uniformes)
- Cargar productos desde la API (con fallback a datos estáticos)
- Tarjetas de producto con imagen, nombre, precio, tallas disponibles
- Filtro por categoría (tabs o select)

#### Fase 6: Carrito de compras
- Icono de carrito en header con contador
- Drawer lateral con items del carrito
- Añadir/quitar productos
- Seleccionar talla y color antes de añadir
- Persistencia en localStorage

#### Fase 7: Formulario de pedido (checkout)
- Formulario paso a paso:
  1. Resumen del carrito
  2. Datos del cliente (nombre, teléfono, dirección)
  3. Notas adicionales
- Al enviar: POST a `/api/orders` + abre WhatsApp con resumen
- Confirmación visual del pedido

#### Fase 8: Testimonios dinámicos
- Carrusel de testimonios cargados desde `GET /api/testimonials`
- Fallback a `opiniones.json` local si la API no responde
- Diseño responsive

#### Fase 9: Mejoras visuales y UX
- Animaciones con Intersection Observer (fade-in, slide-up)
- Lazy loading de imágenes
- Estados de carga (skeleton loaders)
- Mensajes de error amigables si falla la API
- Modo offline parcial (datos cacheados)

#### Fase 10: SEO y rendimiento
- Meta tags mejorados
- Open Graph para compartir en redes
- Sitemap básico
- Optimización de imágenes (WebP)
- Puntuación Lighthouse > 90

---

## Orden de ejecución recomendado

```
Semana 1: Fase 1 (backend base) + Fase 5 (catálogo frontend)
Semana 2: Fase 2 (API pública) + Fase 6 (carrito frontend)
Semana 3: Fase 3 (auth + admin) + Fase 7 (checkout frontend)
Semana 4: Fase 4 (deploy backend) + Fase 8 (testimonios)
Semana 5: Fases 9 y 10 (pulido y SEO)
```

---

## Stack de tecnologías

| Componente | Tecnología |
|------------|-----------|
| Frontend   | HTML5, CSS3, JavaScript vanilla |
| Backend    | Python 3.11+, FastAPI, Uvicorn |
| ORM        | SQLAlchemy 2.0 |
| Migraciones | Alembic |
| Base de datos | PostgreSQL 15 |
| Auth       | JWT (python-jose + passlib) |
| Templates admin | Jinja2 |
| Hosting frontend | Vercel |
| Hosting backend | Render o Railway |
| Control de versiones | GitHub |

---

## Notas importantes

- El frontend funciona 100% en estático, no requiere build step
- El carrito y la lógica de pedidos corren del lado del cliente
- La API del backend es opcional para funcionalidad básica (fallback a datos locales)
- Las imágenes de productos se sirven desde el propio repo en Vercel (no requiere CDN externa)
- El admin panel usa Jinja2 para servir HTML directamente desde FastAPI (no necesita SPA)
