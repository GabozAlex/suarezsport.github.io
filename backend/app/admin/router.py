from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.supabase_db import get_all, get_one, insert, update, delete
from app.auth import verify_password, create_access_token, get_current_user
from app.storage_utils import subir_imagen
import os

router = APIRouter(prefix='/admin', tags=['admin'])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))


def login_required(request: Request):
    return get_current_user(request)


@router.get('/login')
def login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/api/login')
def login(username: str = Form(...), password: str = Form(...)):
    user = get_one('users', {'username': f'eq.{username}'})
    if not user or not verify_password(password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({'sub': user['username']})
    return {'token': token, 'username': user['username']}


@router.get('/dashboard')
def dashboard(request: Request, _=Depends(login_required)):
    products = get_all('products', {'select': 'id'})
    orders = get_all('orders', {'select': 'id'})
    testimonials = get_all('testimonials', {'select': 'id'})
    unread = get_all('contact_messages', {'select': 'id', 'read': 'eq.false'})
    recent_orders = get_all('orders', {'select': '*', 'order': 'created_at.desc', 'limit': '5'})

    stats = {
        'products': len(products),
        'orders': len(orders),
        'testimonials': len(testimonials),
        'messages': len(unread),
    }
    return templates.TemplateResponse('dashboard.html', {
        'request': request,
        'stats': stats,
        'recent_orders': recent_orders,
    })


@router.get('/products')
def list_products_admin(request: Request, _=Depends(login_required)):
    products = get_all('products', {'select': '*', 'order': 'created_at.desc'})
    return templates.TemplateResponse('products.html', {'request': request, 'products': products})


@router.get('/products/new')
def product_form(request: Request, _=Depends(login_required)):
    return templates.TemplateResponse('product_form.html', {'request': request})


@router.post('/products')
def create_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(''),
    category: str = Form(...),
    price: float = Form(...),
    sizes: str = Form(''),
    colors: str = Form(''),
    _=Depends(login_required),
):
    insert('products', {
        'name': name,
        'description': description,
        'category': category,
        'price': price,
        'sizes': [s.strip() for s in sizes.split(',') if s.strip()],
        'colors': [c.strip() for c in colors.split(',') if c.strip()],
        'images': [],
    })
    return RedirectResponse(url='/admin/products', status_code=303)


@router.post('/products/{product_id}/upload')
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    _=Depends(login_required),
):
    product = get_one('products', {'id': f'eq.{product_id}'})
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    url = subir_imagen(file)
    images = list(product.get('images') or [])
    images.append(url)
    update('products', product_id, {'images': images})
    return {'url': url}


@router.post('/products/{product_id}/images/delete')
def delete_product_image(
    product_id: int,
    image_url: str = Form(...),
    _=Depends(login_required),
):
    product = get_one('products', {'id': f'eq.{product_id}'})
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    images = list(product.get('images') or [])
    if image_url in images:
        from urllib.parse import urlparse
        filename = urlparse(image_url).path.rsplit('/', 1)[-1]
        from app.storage_utils import borrar_imagen
        try:
            borrar_imagen(filename)
        except Exception:
            pass
        images.remove(image_url)
        update('products', product_id, {'images': images})
    return RedirectResponse(url=f'/admin/products/{product_id}/edit', status_code=303)


@router.get('/products/{product_id}/edit')
def edit_product_form(
    request: Request,
    product_id: int,
    _=Depends(login_required),
):
    product = get_one('products', {'id': f'eq.{product_id}'})
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return templates.TemplateResponse('product_form.html', {'request': request, 'product': product})


@router.post('/products/{product_id}/edit')
def update_product(
    product_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(''),
    category: str = Form(...),
    price: float = Form(...),
    sizes: str = Form(''),
    colors: str = Form(''),
    _=Depends(login_required),
):
    product = get_one('products', {'id': f'eq.{product_id}'})
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    update('products', product_id, {
        'name': name,
        'description': description,
        'category': category,
        'price': price,
        'sizes': [s.strip() for s in sizes.split(',') if s.strip()],
        'colors': [c.strip() for c in colors.split(',') if c.strip()],
    })
    return RedirectResponse(url='/admin/products', status_code=303)


@router.post('/products/{product_id}/toggle')
def toggle_product(product_id: int, _=Depends(login_required)):
    product = get_one('products', {'id': f'eq.{product_id}'})
    if product:
        update('products', product_id, {'active': not product.get('active', True)})
    return RedirectResponse(url='/admin/products', status_code=303)


@router.post('/products/{product_id}/delete')
def delete_product(product_id: int, _=Depends(login_required)):
    delete('products', product_id)
    return RedirectResponse(url='/admin/products', status_code=303)


@router.get('/orders')
def list_orders_admin(request: Request, _=Depends(login_required)):
    orders = get_all('orders', {'select': '*', 'order': 'created_at.desc'})
    return templates.TemplateResponse('orders.html', {'request': request, 'orders': orders})


@router.post('/orders/{order_id}/status')
def update_order_status(
    order_id: int,
    status_val: str = Form(...),
    _=Depends(login_required),
):
    update('orders', order_id, {'status': status_val})
    return RedirectResponse(url='/admin/orders', status_code=303)


@router.post('/orders/{order_id}/delete')
def delete_order(order_id: int, _=Depends(login_required)):
    delete('orders', order_id)
    return RedirectResponse(url='/admin/orders', status_code=303)


@router.get('/testimonials')
def list_testimonials_admin(request: Request, _=Depends(login_required)):
    testimonials = get_all('testimonials', {'select': '*', 'order': 'created_at.desc'})
    return templates.TemplateResponse('testimonials_admin.html', {'request': request, 'testimonials': testimonials})


@router.post('/testimonials/new')
def create_testimonial(
    name: str = Form(...),
    product: str = Form(...),
    opinion: str = Form(...),
    rating: int = Form(...),
    _=Depends(login_required),
):
    insert('testimonials', {
        'name': name,
        'product': product,
        'opinion': opinion,
        'rating': min(max(rating, 1), 5),
        'active': True,
    })
    return RedirectResponse(url='/admin/testimonials', status_code=303)


@router.post('/testimonials/{testimonial_id}/toggle')
def toggle_testimonial(testimonial_id: int, _=Depends(login_required)):
    t = get_one('testimonials', {'id': f'eq.{testimonial_id}'})
    if t:
        update('testimonials', testimonial_id, {'active': not t.get('active', False)})
    return RedirectResponse(url='/admin/testimonials', status_code=303)


@router.post('/testimonials/{testimonial_id}/delete')
def delete_testimonial(testimonial_id: int, _=Depends(login_required)):
    delete('testimonials', testimonial_id)
    return RedirectResponse(url='/admin/testimonials', status_code=303)


@router.get('/messages')
def list_messages_admin(request: Request, _=Depends(login_required)):
    messages = get_all('contact_messages', {'select': '*', 'order': 'created_at.desc'})
    return templates.TemplateResponse('messages.html', {'request': request, 'messages': messages})


@router.post('/messages/{message_id}/read')
def toggle_message_read(message_id: int, _=Depends(login_required)):
    msg = get_one('contact_messages', {'id': f'eq.{message_id}'})
    if msg:
        update('contact_messages', message_id, {'read': not msg.get('read', False)})
    return RedirectResponse(url='/admin/messages', status_code=303)


@router.post('/messages/{message_id}/delete')
def delete_message(message_id: int, _=Depends(login_required)):
    delete('contact_messages', message_id)
    return RedirectResponse(url='/admin/messages', status_code=303)


@router.get('/api/setup')
def setup_admin():
    from app.auth import hash_password
    try:
        existing = get_one('users', {'username': 'eq.admin'})
        if existing:
            return {'message': 'Admin already exists'}
        insert('users', {
            'username': 'admin',
            'hashed_password': hash_password('admin123'),
            'is_admin': True,
        })
        return {'message': 'Admin created — user: admin, pass: admin123'}
    except Exception as e:
        return {'error': str(e), 'type': type(e).__name__}
