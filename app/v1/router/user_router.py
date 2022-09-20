from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Body
from fastapi.security import OAuth2PasswordRequestForm

from app.v1.schema import user_schema
from app.v1.service import user_service
from app.v1.service import auth_service
from app.v1.schema.token_schema import Token, TokenData

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

@router.post(
    "/login",
    tags=["users"],
    response_model=Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = auth_service.generate_token(form_data.username, form_data.password)
    return Token(access_token=access_token, token_type="bearer")
