from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import userschema, login_schema, forgot_password_schema, generic_schema
from app.services import auth_service
from app.docs.auth_responses import responses_docs, login_responses, password_responses
from datetime import timedelta
from app.dependencies import get_current_user  # <--- IMPORT NOVO
from app.models.users import User

router = APIRouter(
  prefix="/autenticacao",
  tags=["Authentication"]
)

@router.post(
  "/cadastro", 
  status_code=status.HTTP_201_CREATED, 
  response_model=userschema.UserResponse,
  responses=responses_docs
)
def cadastro(user: userschema.UserCreate, db: Session = Depends(get_db)):
  """
  Registra um novo usuário no sistema.
  - Valida idade (18+)
  - Valida formato de telefone
  - Valida senha (6+ chars)
  - Exige aceite dos termos
  """

  return auth_service.create_user(db=db, user_input=user)

@router.post(
  "/login", 
  response_model=login_schema.Token,
  responses=login_responses
)
def login(login_data: login_schema.UserLogin, db: Session = Depends(get_db)):
  """
  Realiza o login do usuário.
  - Verifica credenciais.
  - Bloqueia após 3 tentativas erradas (30s).
  - Retorna Token JWT (Bearer).
  """
  user = auth_service.authenticate_user(db, login_data)
  validade_token = timedelta(minutes=30)

  if login_data.remember_me:
    validade_token = timedelta(hours=24)

  # TODO melhorar a criação do token aplicando cookies com http only, secure e samssie para evitar xss e ataques CSRF
  access_token = auth_service.create_access_token(
    data={"sub": user.email},
    expires_delta=validade_token
  )
  
  return {
    "access_token": access_token,
    "user_id": user.id,
    "username": user.username
  }

@router.post(
  "/esqueceu-senha/solicitar", 
  response_model=generic_schema.MessageResponse,
  responses=password_responses
)
def solicitar_codigo(data: forgot_password_schema.ForgotPasswordRequest, db: Session = Depends(get_db)):
  """
  Passo 1: Usuário informa e-mail e recebe o código.
  """
  return auth_service.request_password_reset(db, data.email)

@router.post(
  "/esqueceu-senha/redefinir", 
  response_model=generic_schema.MessageResponse,
  responses=password_responses
)
def redefinir_senha_com_codigo(data: forgot_password_schema.ResetPasswordRequest, db: Session = Depends(get_db)):
  """
  Passo 2: Usuário envia E-mail + Código + Nova Senha.
  - O sistema valida tudo e altera a senha se estiver correto.
  """
  return auth_service.reset_password(db, data)

@router.get("/me", response_model=userschema.UserResponse)
def ler_dados_do_usuario_atual(current_user: User = Depends(get_current_user)):
  """
  Retorna os dados do usuário logado.
  🔒 Exige Autenticação (Token JWT).
  """
  return current_user
