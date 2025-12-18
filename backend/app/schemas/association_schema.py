from pydantic import BaseModel
from typing import Literal

class AssociationRequest(BaseModel):
  item_type: Literal["RN", "US", "RF", "RNF"]
  item_id: int
