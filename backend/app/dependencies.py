from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# atualiza no swagger a rota como protegida e destiva tratamento automatico para personalizar o retorno do erro
security = HTTPBearer(auto_error=False)

def get_current_user(
  creds: HTTPAuthorizationCredentials = Depends(security), 
  db: Session = Depends(get_db)
):
  if not creds:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Não autenticado"
    )

  token = creds.credentials

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não foi possível validar as credenciais"
  )
  
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    
    if email is None:
      raise credentials_exception
          
  except JWTError:
    raise credentials_exception

  user = db.query(User).filter(User.email == email).first()
  
  if user is None:
    raise credentials_exception

  return user
