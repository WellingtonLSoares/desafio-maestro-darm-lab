from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import date
import re

from app.models.users import User
from app.models.user_term import UserTerm
from app.schemas import userschema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return pwd_context.hash(password)

def create_user(db: Session, user_input: userschema.UserCreate):
  if not user_input.email or not user_input.password or not user_input.full_name:
    raise HTTPException(status_code=400, detail="Campos obrigatórios não preenchidos")

  user_exists = db.query(User).filter(User.email == user_input.email).first()
  
  if user_exists:
    raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

  if len(user_input.password) < 6:
    raise HTTPException(status_code=400, detail="Insira pelo menos 6 caracteres na senha.")

  # (XX) XXXXX-XXXX ou (XX) XXXX-XXXX 
  phone_pattern = re.compile(r"^\(\d{2}\) \d{4,5}-\d{4}$")
  if not phone_pattern.match(user_input.phone_number):
    raise HTTPException(status_code=400, detail="Telefone inválido. Use o formato (XX) XXXXX-XXXX.")

  today = date.today()
  age = today.year - user_input.birth_date.year - (
    (today.month, today.day) < (user_input.birth_date.month, user_input.birth_date.day)
  )
  
  if age < 18:
    raise HTTPException(status_code=400, detail="Idade mínima para cadastro é de 18 anos.")

  if not user_input.terms_accepted:
    raise HTTPException(status_code=400, detail="Você precisa aceitar os Termos de Serviço para continuar.")

  try:
    new_user = User(
      full_name=user_input.full_name,
      username=user_input.email.split("@")[0],
      email=user_input.email,
      phone_number=user_input.phone_number,
      birth_date=user_input.birth_date,
      hashed_password=get_password_hash(user_input.password)
    )
    db.add(new_user)
    db.flush()

    user_term = UserTerm(
      user_id=new_user.id,
      terms_accepted=True,
    )
    db.add(user_term)

    db.commit()
    db.refresh(new_user)

    return new_user

  except Exception as e:
    db.rollback()
    error = str(e)

    # trocar por logs
    print(error)

    raise HTTPException(status_code=500, detail="Erro interno do servidor ao processar requisição.")
