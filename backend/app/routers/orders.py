from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order
from app.schemas import OrderCreate, OrderOut

router = APIRouter(prefix='/api/orders', tags=['orders'])


@router.post('', response_model=OrderOut, status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    order = Order(
        customer_name=data.customer_name,
        phone=data.phone,
        address=data.address,
        items=data.items,
        total=data.total,
        notes=data.notes,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
