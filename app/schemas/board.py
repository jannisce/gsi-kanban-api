from pydantic import BaseModel
from typing import List as PydanticList

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True

class BoardCreate(BaseSchema):
    name: str

class BoardResponse(BoardCreate):
    id: int

class TaskResponse(BaseSchema):
    id: int
    title: str
    description: str | None

class ListResponse(BaseSchema):
    id: int
    name: str
    tasks: PydanticList[TaskResponse]

class FullBoardResponse(BaseSchema):
    id: int
    name: str
    lists: PydanticList[ListResponse]
