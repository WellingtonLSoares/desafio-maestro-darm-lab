from pydantic import BaseModel

class ErrorResponse(BaseModel):
  detail: str

class MessageResponse(BaseModel):
  message: str

us_full_example = {
  "id": 1,
  "display_id": "US01",
  "title": "Como usuário, quero realizar login",
  "description": "O usuário deve ser capaz de logar com email e senha para acessar o sistema.",
  "owner_id": 1,
  "created_at": "2025-12-17T10:00:00",
  "associated_items": [
    {
      "type": "RN",
      "id": 2,
      "display_id": "RN02",
      "title": "Validação de Senha Forte"
    }
  ]
}

error_401_example = {
    "model": ErrorResponse,
    "description": "Não autenticado.",
    "content": {
        "application/json": {
            "example": {"detail": "Não autenticado"}
        }
    }
}

error_404_example = {
  "model": ErrorResponse,
  "description": "História não encontrada.",
  "content": {
    "application/json": {
      "example": {"detail": "História de usuário não encontrada."}
    }
  }
}

# --- RESPOSTAS DAS ROTAS ---

user_story_create_responses = {
  201: {
    "description": "História de Usuário criada com sucesso.",
    "content": {
      "application/json": {
        "example": us_full_example
      }
    },
  },
  400: {
    "model": ErrorResponse,
    "description": "Erro de validação.",
    "content": {
      "application/json": {
        "examples": {
          "titulo_duplicado": {
            "summary": "Título em uso",
            "value": {"detail": "O título já está em uso."}
          },
          "auto_associacao": {
            "summary": "Auto-associação",
            "value": {"detail": "Não é permitido associar um item a si mesmo."}
          }
        }
      }
    }
  },
  401: error_401_example
}

user_story_list_responses = {
  200: {
    "description": "Listagem paginada retornada com sucesso.",
    "content": {
      "application/json": {
        "example": {
          "total": 1,
          "items": [us_full_example],
          "skip": 0,
          "limit": 10
        }
      }
    }
  },
  401: error_401_example
}

user_story_update_responses = {
  200: {
    "description": "História de Usuário atualizada com sucesso.",
    "content": {
      "application/json": {
        "example": us_full_example
      }
    }
  },
  400: {
    "model": ErrorResponse,
    "description": "Erro de validação.",
    "content": {
      "application/json": {
        "examples": {
          "titulo_duplicado": {
            "summary": "Título em uso",
            "value": {"detail": "O título já está em uso."}
          }
        }
      }
    }
  },
  401: error_401_example,
  404: error_404_example
}

user_story_delete_responses = {
  200: {
    "model": MessageResponse,
    "description": "História excluída com sucesso.",
    "content": {
      "application/json": {
        "example": {"message": "História excluída com sucesso."}
      }
    }
  },
  401: error_401_example,
  404: error_404_example
}
