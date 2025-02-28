from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Board(Base):
    __tablename__ = "boards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    lists = relationship("List", back_populates="board", cascade="all, delete")
