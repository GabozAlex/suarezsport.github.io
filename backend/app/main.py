from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routers import products, testimonials, orders, contact
from app.admin.router import router as admin_router
import os

app = FastAPI(title='Suarez Sport API', docs_url='/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(products.router)
app.include_router(testimonials.router)
app.include_router(orders.router)
app.include_router(contact.router)
app.include_router(admin_router)

static_dir = os.path.join(os.path.dirname(__file__), 'admin', 'static')
app.mount('/admin/static', StaticFiles(directory=static_dir), name='admin_static')


@app.get('/api/categories')
def get_categories():
    return ['camisas', 'short', 'conjuntos', 'sueter', 'accesorios', 'uniformes']


@app.get('/admin/logout')
def logout():
    resp = RedirectResponse(url='/admin/login', status_code=303)
    resp.delete_cookie('token')
    return resp


@app.get('/')
def root():
    from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_BUCKET
    return {
        'message': 'Suarez Sport API',
        'docs': '/docs',
        'admin': '/admin/login',
        'supabase_configured': bool(SUPABASE_URL and SUPABASE_SERVICE_KEY),
        'supabase_bucket': SUPABASE_BUCKET,
    }
