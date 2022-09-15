from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Body

from app.v1.schema import user_schema
from app.v1.service import user_service

from app.v1.utils.db import get_db

router = APIRouter(prefix='/api/v1')

@router.post(
    '/user/',
    tags = ['users'],
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.User,
    dependencies=[Depends(get_db)],
    summary="Usuario creado"   
)
def create_user(user: user_schema.UserRegister = Body(...)):
    """Ejecuta la función creada en service

    Args:
        user (user_schema.UserRegister, optional): Usuario a crear

    Returns:
        json: usuario crado
    """
    return user_service.create_user(user)