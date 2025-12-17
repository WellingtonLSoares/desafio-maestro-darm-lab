from app.schemas import login_schema, generic_schema

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

password_responses = {
  200: {
    "description": "Operação realizada com sucesso",
    "model": generic_schema.MessageResponse
  },
  400: {
    "description": "Erro de validação (Código inválido/expirado)",
    "content": {
      "application/json": {
        "example": {"detail": "O código expirou. Solicite um novo."}
      }
    }
  },
  403: {
    "description": "Bloqueio temporário",
    "content": {
      "application/json": {
        "example": {"detail": "Muitas tentativas falhas. Tente novamente em 30 minutos."}
      }
    }
  },
  404: {
    "description": "Recurso não encontrado",
    "content": {
      "application/json": {
        "example": {"detail": "E-mail não encontrado no sistema."}
      }
    }
  }
}
