from fastapi import HTTPException, status

from app.v1.schema import todo_schema
from app.v1.schema import user_schema

from app.v1.model.todo_model import Todo as TodoModel 

def create_task(task: todo_schema.TodoCreate, user: user_schema.User):
    """Crea una tarea en la base de datos

    Args:
        task (todo_schema.TodoCreate): Tarea a crear
        user (user_schema.User): Usuario creador

    Returns:
        json: Información de tarea creada
    """
    
    db_task = TodoModel(
        title= task.title,
        user_id = user.id
    )
    
    db_task.save()
    
    return todo_schema.Todo(
        id = db_task.id,
        title=db_task.title,
        is_done=db_task.is_done,
        create_at= db_task.create_at
    )
    
def get_tasks(user: user_schema.User, is_done: bool = None):
    
    if is_done is None:
        task_by_user = TodoModel.filter(TodoModel.user_id == user.id).order_by(TodoModel.create_at.desc())
    else:
        task_by_user = TodoModel.filter((TodoModel.user_id  == user.id) & (TodoModel.is_done == is_done)).order_by(TodoModel.create_at.desc())
        
    list_tasks = []
    for task in task_by_user:
        list_tasks.append(
            todo_schema.Todo(
                id = task.id,
                title=task.title,
                is_done=task.is_done,
                create_at=task.create_at
            )
        )
        
    return list_tasks

def get_task(task_id: int, user: user_schema.User):
    task = TodoModel.filter(
        (TodoModel.id == task_id) & (TodoModel.user_id == user.id)
        ).get()
    
    return todo_schema.Todo(
        id = task.id,
        title = task.title,
        is_done= task.is_done,
        create_at = task.create_at
    )
    
def update_status_task(is_done: bool, task_id: int, user: user_schema.User):
    task = TodoModel.filter(
        (TodoModel.id == task_id) & ( TodoModel.user_id == user.id)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la tarea"
        )
    
    task.is_done = is_done
    task.save()
    
    return todo_schema.Todo(
        id = task.id,
        title = task.title,
        is_done = task.is_done,
        create_at= task.create_at
    )    
    
def delete_task(task_id:int, user: user_schema.User):
    task = TodoModel.filter(
        (TodoModel.id == task_id) & (TodoModel.user_id == user.id)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la tarea"
        )
        
    task.delete_instance()
    
    