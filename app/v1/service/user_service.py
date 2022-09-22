from fastapi import HTTPException, status

from app.v1.service.auth_service import get_password_hash
from app.v1.model.user_model import User as UserModel
from app.v1.schema import user_schema



def create_user(user: user_schema.UserRegister):
    """Esta función me permite crear un usuario en la base de datos a través de un método post

    Args:
        user (user_schema.UserRegister): usuario a crear

    Raises:
        HTTPException: Error cuándo la petición no satisface las condiciones

    Returns:
        json: Usuario creado
    """
    
    get_user = UserModel.filter(
        (UserModel.email == user.email) | (UserModel.username == user.username)
        )
    if get_user:
        msg = "El email ya está creado"
        if get_user.get().username == user.username:
            msg = "Usuario ya creado"
    
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = msg
        )
    
    db_user = UserModel(
        username = user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    db_user.save()
    
    return user_schema.User(
        id = db_user.id,
        username = db_user.username,
        email = db_user.email
    )