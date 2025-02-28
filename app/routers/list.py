from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.board import Board
from app.models.list import List

from app.schemas.list import ListCreate, ListUpdate, ListResponse, PydanticList

import app.dependencies as dependencies

router = APIRouter(prefix="/lists", tags=["Lists"])

# Create List
@router.post("/", response_model=ListResponse, status_code=201)
def create_list(list_data: ListCreate, db: Session = Depends(dependencies.get_db)):
    # Check if the board exists
    board_exists = db.query(Board).filter(Board.id == list_data.board_id).first()
    if not board_exists:
        raise HTTPException(status_code=400, detail="Board does not exist")
    db_list = List(name=list_data.name, board_id=list_data.board_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

# Get All Lists
@router.get("/", response_model=PydanticList[ListResponse])
def get_lists(db: Session = Depends(dependencies.get_db)):
    return db.query(List).all()

# Get List by ID
@router.get("/{list_id}", response_model=ListResponse)
def get_list(list_id: int, db: Session = Depends(dependencies.get_db)):
    db_list = db.query(List).filter(List.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    return db_list

# Update List
@router.put("/{list_id}", response_model=ListResponse)
def update_list(list_id: int, list_data: ListUpdate, db: Session = Depends(dependencies.get_db)):
    db_list = db.query(List).filter(List.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")

    # Update only provided fields
    if list_data.name is not None:
        db_list.name = list_data.name
    if list_data.board_id is not None:
        db_list.board_id = list_data.board_id

    db.commit()
    db.refresh(db_list)
    return db_list

# Delete List
@router.delete("/{list_id}", status_code=204)
def delete_list(list_id: int, db: Session = Depends(dependencies.get_db)):
    db.query(List).filter(List.id == list_id).delete()
    db.commit()
