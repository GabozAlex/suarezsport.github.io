from fastapi import APIRouter, HTTPException, status
from app.supabase_db import insert, get_one
from pydantic import BaseModel

router = APIRouter(prefix='/api/orders', tags=['orders'])


class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    address: str
    items: list
    total: float
    notes: str = ''


@router.post('', status_code=201)
def create_order(data: OrderCreate):
    if not data.customer_name.strip():
        raise HTTPException(status_code=400, detail='El nombre del cliente es obligatorio')
    if not data.items or not isinstance(data.items, list) or len(data.items) == 0:
        raise HTTPException(status_code=400, detail='El pedido debe tener al menos un producto')
    if data.total <= 0:
        raise HTTPException(status_code=400, detail='El total debe ser mayor a 0')
    result = insert('orders', data.model_dump())
    if isinstance(result, list) and len(result) > 0:
        return result[0]
    return result
