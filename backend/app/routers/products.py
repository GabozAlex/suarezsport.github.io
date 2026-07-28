from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.schemas import ProductOut

router = APIRouter(prefix='/api/products', tags=['products'])


@router.get('', response_model=list[ProductOut])
def list_products(
    category: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Product).filter(Product.active == True)
    if category:
        q = q.filter(Product.category == category)
    if search:
        q = q.filter(Product.name.ilike(f'%{search}%'))
    return q.order_by(Product.created_at.desc()).all()


@router.get('/{product_id}', response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.active == True).first()
    if not product:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    return product
