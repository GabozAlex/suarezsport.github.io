from app.database import SessionLocal
from app.models import User
from app.auth import hash_password
import sys


def crear_admin(username: str, password: str):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            print(f'El usuario "{username}" ya existe.')
            return
        user = User(username=username, hashed_password=hash_password(password))
        db.add(user)
        db.commit()
        print(f'Admin "{username}" creado correctamente.')
    finally:
        db.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Uso: python -m app.create_admin <username> <password>')
        sys.exit(1)
    crear_admin(sys.argv[1], sys.argv[2])
