from sqlalchemy.orm import Session, load_only
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import date, datetime, timezone, timedelta
import re
import os
from jose import jwt
from dotenv import load_dotenv

from app.models.users import User
from app.models.user_term import UserTerm
from app.schemas import userschema, login_schema

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

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

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
  to_encode.update({"exp": expire})
  
  if not SECRET_KEY:
    raise HTTPException(status_code=500, detail="Erro de configuração: SECRET_KEY não definida.")

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def authenticate_user(db: Session, login_data: login_schema.UserLogin):
  LOCKOUT_DURATION_SECONDS = 30
  user = db.query(User).filter(User.email == login_data.email).options(load_only(
    User.id,
    User.username,
    User.email,
    User.hashed_password,
    User.failed_login_attempts,
    User.last_failed_login
  )).first()

  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Usuário ou senha incorretos"
    )

  if user.failed_login_attempts >= 3:
    if user.last_failed_login:
      last_fail = user.last_failed_login

      if last_fail.tzinfo is None:
        last_fail = last_fail.replace(tzinfo=timezone.utc)
          
      time_since_last_fail = datetime.now(timezone.utc) - last_fail
      
      if time_since_last_fail.total_seconds() < LOCKOUT_DURATION_SECONDS:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN, 
          detail=f"Você possui 3 tentativas. Conta bloqueada por {LOCKOUT_DURATION_SECONDS}s."
        )
      else:
        user.failed_login_attempts = 0
        db.commit()

  if not verify_password(login_data.password, user.hashed_password):
    user.failed_login_attempts += 1
    user.last_failed_login = datetime.now(timezone.utc)
    db.commit()

    if user.failed_login_attempts >= 3:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail=f"Você possui 3 tentativas. Conta bloqueada por {LOCKOUT_DURATION_SECONDS}s."
      )
    
    # Senha errada -> 401
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Usuário ou senha incorretos"
    )

  user.failed_login_attempts = 0
  db.commit()

  return user
