from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, Enum as SAEnum
from sqlalchemy.sql import func
from app.database import Base
import enum


class OrderStatus(str, enum.Enum):
    pendiente = 'pendiente'
    confirmado = 'confirmado'
    enviado = 'enviado'
    entregado = 'entregado'


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default='')
    category = Column(String(50), nullable=False, index=True)
    price = Column(Float, nullable=False)
    images = Column(JSON, default=list)
    sizes = Column(JSON, default=list)
    colors = Column(JSON, default=list)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    items = Column(JSON, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(SAEnum(OrderStatus), default=OrderStatus.pendiente)
    notes = Column(Text, default='')
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Testimonial(Base):
    __tablename__ = 'testimonials'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    product = Column(String(200), default='')
    opinion = Column(Text, nullable=False)
    rating = Column(Integer, default=5)
    active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContactMessage(Base):
    __tablename__ = 'contact_messages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_admin = Column(Boolean, default=True)
