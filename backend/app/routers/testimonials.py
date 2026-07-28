from fastapi import APIRouter
from app.supabase_db import get_all

router = APIRouter(prefix='/api/testimonials', tags=['testimonials'])


@router.get('')
def list_testimonials():
    return get_all('testimonials', {
        'select': '*',
        'active': 'eq.true',
        'order': 'created_at.desc',
    })
