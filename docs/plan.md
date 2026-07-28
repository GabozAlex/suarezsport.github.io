# Plan de Ejecución — Suarez Sport Web Completa

## Estado actual (Julio 2026)

### ✅ Completado
- Fase 1: Catálogo dinámico con 58 productos, tabs de filtro, grid responsive
- Fase 2: Carrito con drawer, modal talla/color, localStorage
- Fase 3: Checkout paso a paso dentro del drawer → WhatsApp
- Fase 4: Testimonios dinámicos con carrusel + fallback local
- Fase 5: Animaciones scroll, skeleton loaders, lazy loading
- Fase 6: SEO completo (OG, Twitter Cards, JSON-LD, sitemap, robots.txt)
- Fase 7: Backend FastAPI + admin Jinja2 + Supabase REST + Storage
- Frontend conectado a API real con fallback local
- Deploy: Backend en Render, Frontend en Vercel

### 🔲 Pendientes

| # | Tarea | Prioridad |
|---|-------|-----------|
| 1 | **Multi-categoría** — Cambiar `category` único a `categories` array para que un producto esté en varias categorías | Media |
| 2 | **Más categorías** — Agregar nuevas categorías como `personalizados`, `nuevos`, `ofertas` cuando el negocio lo requiera | Baja |

### ✅ Recién agregado

- **Paginación** — 12 productos por página con botones numéricos, por categoría
- **Contador de vistas** — Se incrementa al abrir el modal de un producto, visible en admin
- **Subir imágenes desde admin** — Upload + delete en el form de producto
- **Crear testimonios desde admin** — Formulario en la página de testimonios
- **WhatsApp flotante** — Botón fijo con pulso en la landing
- **Buscador de productos** — Filtro por nombre en tiempo real
- **Galería de clientes** — Sección con imágenes de clientes
- **Script migración** — `backend/scripts/migrar_productos.py`

---

## Arquitectura actual

```
suarezsport.github.io/     → Frontend (HTML/CSS/JS)          → Vercel
  ├── index.html
  ├── css/index.css
  ├── js/
  │   ├── script.js          → Lógica frontend
  │   ├── productos.js       → 58 productos (fallback local)
  │   └── config.js          → API_URL
  ├── imagenes/...
  └── docs/...

backend/                     → Backend (FastAPI + Supabase)   → Render
  ├── app/
  │   ├── main.py            → FastAPI app
  │   ├── config.py          → Variables de entorno
  │   ├── supabase_db.py     → Wrapper REST Supabase
  │   ├── auth.py            → JWT + hash
  │   ├── storage_utils.py   → Supabase Storage
  │   ├── routers/           → API pública
  │   └── admin/             → Admin panel Jinja2
  ├── Dockerfile
  └── requirements.txt
```

## API endpoints

### Públicos
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/products` | Listar productos (?category=, ?search=) |
| GET | `/api/products/{id}` | Detalle |
| GET | `/api/categories` | Categorías |
| POST | `/api/orders` | Crear pedido |
| GET | `/api/testimonials` | Testimonios activos |
| POST | `/api/contact` | Contacto |

### Admin
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/admin/login` | Login |
| GET | `/admin/dashboard` | Stats |
| CRUD | `/admin/products` | Productos |
| POST | `/admin/products/{id}/upload` | Subir imagen |
| POST | `/admin/products/{id}/images/delete` | Borrar imagen |
| GET/POST | `/admin/orders` | Pedidos |
| CRUD | `/admin/testimonials` | Testimonios |
| GET/POST | `/admin/messages` | Mensajes |
