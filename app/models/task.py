from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"))
    
    list = relationship("List", back_populates="tasks")
