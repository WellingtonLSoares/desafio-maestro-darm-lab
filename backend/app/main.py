from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
  title="DARM Labs Challenge API",
  description="API para gerenciamento de Requisitos (Histórias de Usuário e Regras de Negócio).",
  version="1.0.0"
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

@app.get("/")
def read_root():
  return {"message": "API DARM Labs está rodando!"}
