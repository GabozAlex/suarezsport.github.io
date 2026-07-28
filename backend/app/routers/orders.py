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
    result = insert('orders', data.model_dump())
    if isinstance(result, list) and len(result) > 0:
        return result[0]
    return result
