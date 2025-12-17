from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class UserTerm(Base):
  __tablename__ = "user_terms"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
  terms_accepted = Column(Boolean, default=True, nullable=False)
  terms_accepted_at = Column(DateTime(timezone=True), server_default=func.now())
  
  user = relationship("User", back_populates="term_agreement")