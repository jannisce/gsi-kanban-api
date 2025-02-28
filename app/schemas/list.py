from pydantic import BaseModel
from typing import Optional, List as PydanticList

class ListCreate(BaseModel):
    name: str
    board_id: int

class ListUpdate(BaseModel):
    name: Optional[str] = None
    board_id: Optional[int] = None

class ListResponse(ListCreate):
    id: int
