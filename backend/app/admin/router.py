from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Order, Testimonial, ContactMessage, User, OrderStatus
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.storage_utils import subir_imagen
from app.schemas import ProductUpdate
import os

router = APIRouter(prefix='/admin', tags=['admin'])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))


def login_required(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get('token')
    if not token:
        raise HTTPException(status_code=303, detail='Not authenticated')
    from jose import JWTError, jwt
    from app.config import SECRET_KEY, ALGORITHM
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=303, detail='User not found')
        return user
    except JWTError:
        raise HTTPException(status_code=303, detail='Invalid token')


@router.get('/login')
def login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/api/login')
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({'sub': user.username})
    return {'token': token, 'username': user.username}


@router.get('/dashboard')
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    stats = {
        'products': db.query(Product).count(),
        'orders': db.query(Order).count(),
        'testimonials': db.query(Testimonial).count(),
        'messages': db.query(ContactMessage).filter(ContactMessage.read == False).count(),
    }
    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(5).all()
    return templates.TemplateResponse('dashboard.html', {
        'request': request,
        'stats': stats,
        'recent_orders': recent_orders,
    })


# ─── Products ───

@router.get('/products')
def list_products_admin(
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    products = db.query(Product).order_by(Product.created_at.desc()).all()
    return templates.TemplateResponse('products.html', {'request': request, 'products': products})


@router.get('/products/new')
def product_form(
    request: Request,
    _=Depends(login_required),
):
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
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    product = Product(
        name=name,
        description=description,
        category=category,
        price=price,
        sizes=[s.strip() for s in sizes.split(',') if s.strip()],
        colors=[c.strip() for c in colors.split(',') if c.strip()],
        images=[],
    )
    db.add(product)
    db.commit()
    return RedirectResponse(url='/admin/products', status_code=303)


@router.post('/products/{product_id}/upload')
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    url = subir_imagen(file)
    images = list(product.images or [])
    images.append(url)
    product.images = images
    db.commit()
    return {'url': url}


@router.get('/products/{product_id}/edit')
def edit_product_form(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    product = db.query(Product).filter(Product.id == product_id).first()
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
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    product.name = name
    product.description = description
    product.category = category
    product.price = price
    product.sizes = [s.strip() for s in sizes.split(',') if s.strip()]
    product.colors = [c.strip() for c in colors.split(',') if c.strip()]
    db.commit()
    return RedirectResponse(url='/admin/products', status_code=303)


@router.post('/products/{product_id}/toggle')
def toggle_product(product_id: int, db: Session = Depends(get_db), _=Depends(login_required)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.active = not product.active
        db.commit()
    return RedirectResponse(url='/admin/products', status_code=303)


@router.post('/products/{product_id}/delete')
def delete_product(product_id: int, db: Session = Depends(get_db), _=Depends(login_required)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return RedirectResponse(url='/admin/products', status_code=303)


# ─── Orders ───

@router.get('/orders')
def list_orders_admin(
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return templates.TemplateResponse('orders.html', {'request': request, 'orders': orders})


@router.post('/orders/{order_id}/status')
def update_order_status(
    order_id: int,
    status_val: str = Form(...),
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = OrderStatus(status_val)
        db.commit()
    return RedirectResponse(url='/admin/orders', status_code=303)


@router.post('/orders/{order_id}/delete')
def delete_order(order_id: int, db: Session = Depends(get_db), _=Depends(login_required)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return RedirectResponse(url='/admin/orders', status_code=303)


# ─── Testimonials ───

@router.get('/testimonials')
def list_testimonials_admin(
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    testimonials = db.query(Testimonial).order_by(Testimonial.created_at.desc()).all()
    return templates.TemplateResponse('testimonials_admin.html', {'request': request, 'testimonials': testimonials})


@router.post('/testimonials/{testimonial_id}/toggle')
def toggle_testimonial(testimonial_id: int, db: Session = Depends(get_db), _=Depends(login_required)):
    t = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if t:
        t.active = not t.active
        db.commit()
    return RedirectResponse(url='/admin/testimonials', status_code=303)


@router.post('/testimonials/{testimonial_id}/delete')
def delete_testimonial(testimonial_id: int, db: Session = Depends(get_db), _=Depends(login_required)):
    t = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if t:
        db.delete(t)
        db.commit()
    return RedirectResponse(url='/admin/testimonials', status_code=303)


# ─── Messages ───

@router.get('/messages')
def list_messages_admin(
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(login_required),
):
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return templates.TemplateResponse('messages.html', {'request': request, 'messages': messages})


@router.post('/messages/{message_id}/read')
def toggle_message_read(message_id: int, db: Session = Depends(get_db), _=Depends(login_required)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if msg:
        msg.read = not msg.read
        db.commit()
    return RedirectResponse(url='/admin/messages', status_code=303)


@router.post('/messages/{message_id}/delete')
def delete_message(message_id: int, db: Session = Depends(get_db), _=Depends(login_required)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if msg:
        db.delete(msg)
        db.commit()
    return RedirectResponse(url='/admin/messages', status_code=303)
