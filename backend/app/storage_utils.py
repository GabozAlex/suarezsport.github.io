import requests
import uuid
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_BUCKET


def _headers():
    return {
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/octet-stream',
    }


def subir_imagen(file) -> str:
    ext = file.filename.rsplit('.', 1)[-1] if file.filename else 'png'
    filename = f'{uuid.uuid4().hex}.{ext}'
    upload_url = f'{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{filename}'

    resp = requests.post(upload_url, data=file.file.read(), headers=_headers())
    resp.raise_for_status()

    public_url = f'{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{filename}'
    return public_url


def borrar_imagen(filename: str):
    delete_url = f'{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{filename}'
    requests.delete(delete_url, headers=_headers())
