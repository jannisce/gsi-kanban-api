from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class List(Base):
    __tablename__ = "lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"))
    
    board = relationship("Board", back_populates="lists")
    tasks = relationship("Task", back_populates="list", cascade="all, delete")
