from fastapi import APIRouter

from db.postgress import fetch_scalar

router = APIRouter()

@router.get('/ping')
def ping():
    return {'ok': True}

@router.get('/ping-db')
def ping_db():
    value = fetch_scalar('SELECT 1')
    return {'db': value}
