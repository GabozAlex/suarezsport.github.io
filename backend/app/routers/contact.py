import time
from fastapi import APIRouter, HTTPException, Request
from app.supabase_db import insert
from pydantic import BaseModel

router = APIRouter(prefix='/api/contact', tags=['contact'])

_rate_limit: dict[str, list[float]] = {}
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX = 5


class ContactCreate(BaseModel):
    name: str
    email: str
    message: str


@router.post('', status_code=201)
def send_message(data: ContactCreate, request: Request):
    client_ip = request.client.host if request.client else 'unknown'
    now = time.time()
    timestamps = _rate_limit.get(client_ip, [])
    timestamps = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
    if len(timestamps) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail='Demasiadas solicitudes. Intenta en 1 minuto.')
    timestamps.append(now)
    _rate_limit[client_ip] = timestamps
    insert('contact_messages', data.model_dump())
    return {'ok': True}
