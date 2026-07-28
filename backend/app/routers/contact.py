from fastapi import APIRouter
from app.supabase_db import insert
from pydantic import BaseModel

router = APIRouter(prefix='/api/contact', tags=['contact'])


class ContactCreate(BaseModel):
    name: str
    email: str
    message: str


@router.post('', status_code=201)
def send_message(data: ContactCreate):
    insert('contact_messages', data.model_dump())
    return {'ok': True}
