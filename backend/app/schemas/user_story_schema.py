from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.association_schema import AssociationRequest, AssociatedItem

class UserStoryCreate(BaseModel):
  title: str = Field(..., min_length=5, description="O Título da história")
  description: str = Field(..., description="Descrição detalhada ou texto rico")
  associations: Optional[List[AssociationRequest]] = []

class UserStoryResponse(BaseModel):
  id: int
  display_id: str
  title: str
  description: str
  owner_id: int
  created_at: datetime
  associated_items: List[AssociatedItem] = []
  
  class Config:
    from_attributes = True

class UserStoryPaginatedResponse(BaseModel):
  total: int
  items: List[UserStoryResponse]
  skip: int
  limit: int

  class Config:
    from_attributes = True
