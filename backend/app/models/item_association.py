from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base

class ItemAssociation(Base):
  __tablename__ = "item_associations"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  
  source_id = Column(Integer, nullable=False, index=True)
  source_type = Column(String(10), nullable=False) # Ex: "US"
  
  target_id = Column(Integer, nullable=False, index=True)
  target_type = Column(String(10), nullable=False) # Ex: "RN", "RF"
  
  created_at = Column(DateTime(timezone=True), server_default=func.now())

  __table_args__ = (
    Index("idx_source", "source_type", "source_id"),
    Index("idx_target", "target_type", "target_id"),
  )
