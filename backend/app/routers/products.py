from fastapi import APIRouter, HTTPException, status
from app.supabase_db import get_all, get_one, update

router = APIRouter(prefix='/api/products', tags=['products'])


@router.get('')
def list_products(category: str = None, search: str = None):
    params = {'select': '*', 'active': 'eq.true', 'order': 'created_at.desc'}
    if category:
        params['category'] = f'eq.{category}'
    if search:
        params['name'] = f'ilike.%{search}%'
    return get_all('products', params)


@router.get('/{product_id}')
def get_product(product_id: int):
    product = get_one('products', {'id': f'eq.{product_id}'})
    if not product or not product.get('active'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    return product


@router.post('/{product_id}/view')
def track_view(product_id: int):
    product = get_one('products', {'id': f'eq.{product_id}'})
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    current = product.get('views', 0) or 0
    update('products', product_id, {'views': current + 1})
    return {'views': current + 1}
