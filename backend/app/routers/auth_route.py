from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import userschema
from app.services import auth_service
from app.docs.auth_responses import responses_docs

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
