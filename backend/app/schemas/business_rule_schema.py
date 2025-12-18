from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.association_schema import AssociationRequest, AssociatedItem

class BusinessRuleBase(BaseModel):
  title: str = Field(..., min_length=5)
  description: str = Field(...)

class BusinessRuleCreate(BusinessRuleBase):
  associations: Optional[List[AssociationRequest]] = []

class BusinessRuleResponse(BusinessRuleBase):
  id: int
  display_id: str
  owner_id: int
  created_at: datetime
  associated_items: List[AssociatedItem] = []

  class Config:
    from_attributes = True

class BusinessRulePaginatedResponse(BaseModel):
  total: int
  items: List[BusinessRuleResponse]
  skip: int
  limit: int
