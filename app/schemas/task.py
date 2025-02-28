from pydantic import BaseModel
from typing import Optional, List as PydanticList

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    list_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    list_id: Optional[int] = None

class TaskResponse(TaskCreate):
    id: int
