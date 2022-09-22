

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

class TodoCreate(BaseModel):
    title: str = Field(
        ...,
        min_lenght = 1,
        max_length=60,
        example = "Tarea"
    )
    
class Todo(TodoCreate):
    id: int = Field(...)
    is_done: bool = Field(default=False)
    create_at: datetime = Field(default=datetime.now())