from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

class UserBase(BaseModel):
    email: EmailStr = Field(
        ..., 
        example = "santiecheva@udea.edu.co"
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length= 50,
        example = 'nombredeUsiario10'
    )
    
class User(UserBase):
    id: int = Field(
        ...,
        example = '5'
    )
    
class UserRegister(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        ejemplo = 'contrasena'
    )
    

    