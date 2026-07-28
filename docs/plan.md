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
| 1 | **Subir imágenes desde el admin** — Formulario con upload a Supabase Storage + vista previa | Alta |
| 2 | **Migrar 58 productos de productos.js a Supabase** — Script que lee el JS y los inserta en la BD | Alta |
| 3 | **WhatsApp flotante** — Botón fijo en la landing con ícono de WhatsApp | Media |
| 4 | **Buscador de productos** — Input de búsqueda que filtra en tiempo real | Media |
| 5 | **Galería de clientes** — Nueva sección con imágenes de `imagenes/clientes/` | Baja |

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
