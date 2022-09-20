
from datetime import datetime, timedelta
from http.client import HTTPException
from app.v1.model.user_model import User as UserModel
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.v1.utils.settings import Settings
from app.v1.schema.token_schema import TokenData

settings = Settings()

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRE_MINUTES = settings.token_expire

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/login")

def verify_password(plain_password, password):
    return pwd_context.verify(plain_password,password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    response = UserModel.filter((UserModel.username == username) | (UserModel.email == username)).get()
    return response
    
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password,user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def generate_token(username, password):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se validaron las credenciales",
            header={"WWW-Authenticate": "Bearer"}
        )
    acces_token_expires = timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": user.username}, expires_delta=acces_token_expires
    )
    
async def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se validaron las credenciales",
            header={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user