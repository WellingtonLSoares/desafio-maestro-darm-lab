from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import auth_route

app = FastAPI(
  title="DARM Labs Challenge API",
  description="API para gerenciamento de Requisitos (Histórias de Usuário e Regras de Negócio).",
  version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  erro = exc.errors()[0]
  msg_original = erro.get("msg")
  
  # Remove o prefixo técnico feio "Value error, " se ele existir
  if "Value error," in msg_original:
    msg_limpa = msg_original.replace("Value error, ", "")
  else:
    msg_limpa = msg_original

  # Se for erro de campo obrigatório (padrão do Pydantic)
  if erro.get("type") == "missing":
    msg_limpa = f"O campo '{erro.get('loc')[-1]}' é obrigatório."

  return JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content={"detail": msg_limpa}
  )

# cors
origins = [
  "http://localhost:3000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(auth_route.router)

@app.get("/")
def read_root():
  return {"message": "API DARM Labs está rodando!"}
