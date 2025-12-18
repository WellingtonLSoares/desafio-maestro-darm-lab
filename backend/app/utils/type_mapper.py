from app.models.user_story import UserStory
from app.models.business_rule import BusinessRule

TYPE_MAP = {
  "US": UserStory,
  "RN": BusinessRule,
}

def get_model_by_type(type_str: str):
  return TYPE_MAP.get(type_str.upper())
