from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.list import List
from app.models.task import Task

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, PydanticList

import app.dependencies as dependencies

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Create Task
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(dependencies.get_db)):
    # Check if the list exists
    list_exists = db.query(List).filter(List.id == task_data.list_id).first()
    if not list_exists:
        raise HTTPException(status_code=400, detail="List does not exist")
    db_task = Task(title=task_data.title, description=task_data.description, list_id=task_data.list_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Get All Tasks
@router.get("/", response_model=PydanticList[TaskResponse])
def get_tasks(db: Session = Depends(dependencies.get_db)):
    return db.query(Task).all()

# Get Task by ID
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(dependencies.get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update Task (Partial Update Allowed)
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(dependencies.get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_data.title is not None:
        db_task.title = task_data.title
    if task_data.description is not None:
        db_task.description = task_data.description
    if task_data.list_id is not None:
        db_task.list_id = task_data.list_id
    
    db.commit()
    db.refresh(db_task)
    return db_task

# Delete Task 
@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(dependencies.get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
