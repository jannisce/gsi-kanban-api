from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.board import Board
from app.models.list import List

from app.schemas.board import BoardCreate, BoardResponse, FullBoardResponse, PydanticList

import app.dependencies as dependencies

router = APIRouter(prefix="/boards", tags=["Boards"])

# Create Board
@router.post("/", response_model=BoardResponse, status_code=201)
def create_board(board: BoardCreate, db: Session = Depends(dependencies.get_db)):
    db_board = Board(name=board.name)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

# Get All Boards
@router.get("/", response_model=PydanticList[BoardResponse])
def get_boards(db: Session = Depends(dependencies.get_db)):
    return db.query(Board).order_by(Board.id.desc()).all()

# Get Board by ID
@router.get("/{board_id}", response_model=BoardResponse)
def get_board(board_id: int, db: Session = Depends(dependencies.get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

# Update Board
@router.put("/{board_id}", response_model=BoardResponse, status_code=200)
def update_board(board_id: int, board: BoardCreate, db: Session = Depends(dependencies.get_db)):
    db_board = db.query(Board).filter(Board.id == board_id).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    db_board.name = board.name
    db.commit()
    db.refresh(db_board)
    return db_board

# Delete Board
@router.delete("/{board_id}", status_code=204)
def delete_board(board_id: int, db: Session = Depends(dependencies.get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    db.delete(board)
    db.commit()
    return

# Get Full Board with Lists and Tasks
@router.get("/{board_id}/full", response_model=FullBoardResponse)
def get_full_board(board_id: int, db: Session = Depends(dependencies.get_db)):
    full_board = db.query(Board).options(joinedload(Board.lists).joinedload(List.tasks)).filter(Board.id == board_id).first()
    if not full_board:
        raise HTTPException(status_code=404, detail="Board not found")
    return full_board
