from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class UserStory(Base):
  __tablename__ = "user_stories"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  
  title = Column(String, unique=True, index=True, nullable=False)
  description = Column(Text, nullable=False)
  
  owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  owner = relationship("User", back_populates="user_stories")

  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())

  @property
  def display_id(self):
    return f"US{self.id:02d}"
