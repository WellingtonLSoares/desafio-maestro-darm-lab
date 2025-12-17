from pydantic import BaseModel
from datetime import date
from pydantic import BaseModel, field_validator
import re

class UserCreate(BaseModel):
  full_name: str
  email: str
  password: str
  phone_number: str
  birth_date: date
  terms_accepted: bool

  @field_validator('email')
  def validar_email(cls, v):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(email_regex, v):
      raise ValueError('Por favor, insira um e-mail válido (ex: nome@dominio.com)')
    return v

class UserResponse(BaseModel):
  id: int
  username: str
  email: str
  full_name: str
  
  class Config:
    from_attributes = True
