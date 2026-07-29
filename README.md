# Suarez Sport

Landing page + tienda online para **Suarez Sport**, marca de ropa deportiva personalizada en Nueva Esparta, Venezuela. Catálogo interactivo, carrito de compras, pedidos por WhatsApp y panel de administración.

## Stack

| Capa | Tecnología |
|------|-----------|
| **Frontend** | HTML + CSS + JavaScript vanilla |
| **Backend** | FastAPI (Python) |
| **Base de datos** | Supabase (PostgreSQL) |
| **Storage** | Supabase Storage (imágenes) |
| **Admin** | Jinja2 templates + JWT auth |
| **Frontend host** | GitHub Pages |
| **Backend host** | Render |

## Funcionalidades

### Landing page
- Catálogo de 58 productos con filtro por categoría y buscador
- Carrito de compras con selección de talla/color
- Checkout → pedido enviado por WhatsApp
- Testimonios dinámicos con carrusel (API + fallback local)
- Galería de clientes, FAQ, formulario de contacto
- Diseño responsive, animaciones scroll, skeleton loaders

### Panel admin (`/admin/login`)
- Dashboard con stats (productos, pedidos, testimonios, mensajes)
- CRUD de productos con subida/borrado de imágenes
- Gestión de pedidos con cambio de estado y detalle expandible
- CRUD de testimonios con toggle activo/inactivo
- Bandeja de mensajes de contacto

### API endpoints
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/products` | Listar productos (filtro por ?category=, ?search=) |
| GET | `/api/products/{id}` | Detalle de producto |
| GET | `/api/categories` | Listar categorías |
| POST | `/api/orders` | Crear pedido |
| GET | `/api/testimonials` | Testimonios activos |
| POST | `/api/contact` | Enviar mensaje de contacto |

## Estructura del proyecto

```
/
├── index.html              # Landing page
├── css/index.css           # Estilos
├── js/
│   ├── config.js           # API_URL
│   ├── productos.js        # 58 productos (fallback local)
│   └── script.js           # Lógica frontend
├── imagenes/               # Assets
├── docs/                   # Documentación
│
backend/
├── app/
│   ├── main.py             # FastAPI app
│   ├── config.py           # Variables de entorno
│   ├── supabase_db.py      # Wrapper Supabase (requests.Session)
│   ├── auth.py             # JWT + hash
│   ├── storage_utils.py    # Supabase Storage
│   ├── routers/            # API pública
│   └── admin/              # Admin panel (router + Jinja2 templates)
├── supabase_schema.sql     # Esquema de BD
├── Dockerfile
└── requirements.txt
```

## Admin por defecto

```
Usuario: admin
Clave:   admin123
```

Para crear el admin inicial, visita `https://<api>/admin/api/setup` después del deploy.

## Desarrollado por

**Gabriel Rosas** — Desarrollador Web
