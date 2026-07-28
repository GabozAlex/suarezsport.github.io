from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: str = ''
    category: str
    price: float
    images: list = []
    sizes: list = []
    colors: list = []
    active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    images: Optional[list] = None
    sizes: Optional[list] = None
    colors: Optional[list] = None
    active: Optional[bool] = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    address: str
    items: list
    total: float
    notes: str = ''


class OrderOut(BaseModel):
    id: int
    customer_name: str
    phone: str
    address: str
    items: list
    total: float
    status: str
    notes: str
    created_at: datetime

    class Config:
        from_attributes = True


class TestimonialOut(BaseModel):
    id: int
    name: str
    product: str
    opinion: str
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    name: str
    email: str
    message: str
