"""
Migra los 58 productos de js/productos.js a la tabla 'products' en Supabase.
Uso: python -m scripts.migrar_productos
Requiere SUPABASE_URL y SUPABASE_SERVICE_KEY en .env
"""
import re
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.supabase_db import insert, get_all
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

PRODUCTOS_JS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'js', 'productos.js')

CATEGORY_MAP = {
    'camisas': 'camisas',
    'short': 'short',
    'conjuntos': 'conjuntos',
    'sueter': 'sueter',
    'accesorios': 'accesorios',
    'uniformes': 'uniformes',
}


def parse_productos_js(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r"\{ id: (\d+), nombre: '([^']+)', categoria: '([^']+)', precio: ([\d.]+), imagen: '([^']+)', tallas: \[([^\]]+)\], colores: \[([^\]]+)\] \}"
    matches = re.findall(pattern, content)
    productos = []
    for m in matches:
        tallas = [t.strip().strip("'") for t in m[5].split(',')]
        colores = [c.strip().strip("'") for c in m[6].split(',')]
        productos.append({
            'name': m[1],
            'category': CATEGORY_MAP.get(m[2], m[2]),
            'price': float(m[3]),
            'images': [m[4]],
            'sizes': tallas,
            'colors': colores,
            'description': '',
            'active': True,
        })
    return productos


def main():
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("ERROR: SUPABASE_URL y SUPABASE_SERVICE_KEY deben estar en .env")
        sys.exit(1)

    productos = parse_productos_js(PRODUCTOS_JS_PATH)
    print(f"Se encontraron {len(productos)} productos en productos.js")

    existing = get_all('products', {'select': 'name'})
    existing_names = {p['name'] for p in existing}

    inserted = 0
    skipped = 0
    for p in productos:
        if p['name'] in existing_names:
            print(f"  SKIP: {p['name']} (ya existe)")
            skipped += 1
            continue
        insert('products', p)
        print(f"  OK: {p['name']} (${p['price']})")
        inserted += 1

    print(f"\nInsertados: {inserted}, Omitidos: {skipped}, Total: {len(productos)}")


if __name__ == '__main__':
    main()
