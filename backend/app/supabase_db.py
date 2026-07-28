from typing import Optional
import requests
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

HEADERS = {
    'apikey': SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation',
}


def _url(table: str) -> str:
    return f'{SUPABASE_URL}/rest/v1/{table}'


def _query_params(params: Optional[dict] = None) -> dict:
    if not params:
        return {}
    q = {}
    for k, v in params.items():
        if v is not None:
            q[k] = v
    return q


def get_all(table: str, params: Optional[dict] = None):
    resp = requests.get(_url(table), headers=HEADERS, params=_query_params(params))
    resp.raise_for_status()
    return resp.json()


def get_one(table: str, filters: dict):
    resp = requests.get(_url(table), headers=HEADERS, params=filters)
    resp.raise_for_status()
    rows = resp.json()
    return rows[0] if rows else None


def insert(table: str, data: dict):
    resp = requests.post(_url(table), headers=HEADERS, json=data)
    resp.raise_for_status()
    return resp.json()


def update(table: str, id: int, data: dict):
    resp = requests.patch(f'{_url(table)}?id=eq.{id}', headers=HEADERS, json=data)
    resp.raise_for_status()
    return resp.json()


def delete(table: str, id: int):
    resp = requests.delete(f'{_url(table)}?id=eq.{id}', headers=HEADERS)
    resp.raise_for_status()
