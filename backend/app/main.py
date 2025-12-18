from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import auth_route, user_story_route, business_rule_route

app = FastAPI(
  title="DARM Labs Challenge API",
  description="API para gerenciamento de Requisitos (Histórias de Usuário e Regras de Negócio).",
  version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  erro = exc.errors()[0]
  tipo_erro = erro.get("type")
  campo = erro.get('loc')[-1]
  msg_original = erro.get("msg")
  
  if tipo_erro == "missing":
    msg_final = f"O campo '{campo}' é obrigatório."
  
  elif tipo_erro == "string_too_short":
    limite = erro.get("ctx", {}).get("min_length")
    msg_final = f"O campo '{campo}' deve ter pelo menos {limite} caracteres."
  
  else:
    msg_final = msg_original.replace("Value error, ", "")

  return JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content={"detail": msg_final}
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
app.include_router(user_story_route.router)
app.include_router(business_rule_route.router)

@app.get("/")
def read_root():
  return {"message": "API DARM Labs está rodando!"}
