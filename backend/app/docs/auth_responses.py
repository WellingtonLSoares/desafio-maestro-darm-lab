from app.schemas import login_schema 

responses_docs = {
  400: {
    "description": "Violação de Regra de Negócio",
    "content": {
      "application/json": {
        "example": {"detail": "Idade mínima para cadastro é de 18 anos."}
      }
    }
  },
  201: {"description": "Usuário criado com sucesso"}
}

login_responses = {
  200: {
    "description": "Login realizado com sucesso",
    "model": login_schema.Token
  },
  401: {
    "description": "Não Autorizado - Credenciais Inválidas",
    "content": {
      "application/json": {
        "example": {"detail": "Usuário ou senha incorretos"}
      }
    }
  },
  403: {
      "description": "Proibido - Conta Bloqueada Temporariamente",
      "content": {
        "application/json": {
          "example": {"detail": "Você possui 3 tentativas. Conta bloqueada por 30s."}
        }
      }
  }
}
