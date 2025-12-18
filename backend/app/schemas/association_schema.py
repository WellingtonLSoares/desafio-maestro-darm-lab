from pydantic import BaseModel
from typing import Literal

class AssociationRequest(BaseModel):
  item_type: Literal["RN", "US", "RF", "RNF"]
  item_id: int

class AssociatedItem(BaseModel):
  type: str
  id: int
  display_id: str
  title: str
