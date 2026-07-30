from typing import Optional
import requests
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY


_session = requests.Session()
_session.headers.update({
    'apikey': SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation',
})


def _url(table: str) -> str:
    return f'{SUPABASE_URL}/rest/v1/{table}'


def _query_params(params: Optional[dict] = None) -> dict:
    if not params:
        return {}
    return {k: v for k, v in params.items() if v is not None}


def get_all(table: str, params: Optional[dict] = None):
    try:
        resp = _session.get(_url(table), params=_query_params(params))
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f'Error al obtener datos de {table}: {e}') from e


def get_one(table: str, filters: dict):
    try:
        resp = _session.get(_url(table), params=filters)
        resp.raise_for_status()
        rows = resp.json()
        return rows[0] if rows else None
    except requests.RequestException as e:
        raise RuntimeError(f'Error al obtener registro de {table}: {e}') from e


def insert(table: str, data: dict):
    try:
        resp = _session.post(_url(table), json=data)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f'Error al insertar en {table}: {e}') from e


def update(table: str, id: int, data: dict):
    try:
        resp = _session.patch(f'{_url(table)}?id=eq.{id}', json=data)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f'Error al actualizar {table} id={id}: {e}') from e


def delete(table: str, id: int):
    try:
        resp = _session.delete(f'{_url(table)}?id=eq.{id}')
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f'Error al eliminar de {table} id={id}: {e}') from e
