from pydantic import BaseModel

class ErrorResponse(BaseModel):
  detail: str

class MessageResponse(BaseModel):
  message: str

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

user_story_create_responses = {
  201: {
    "description": "História de Usuário criada com sucesso.",
    "content": {
      "application/json": {
        "example": {"message": "História de Usuário criada com sucesso!"}
      }
    },
  },
  400: {"model": ErrorResponse, "description": "Erro de validação."},
  401: error_401_example
}

user_story_list_responses = {
  200: {
    "description": "Listagem paginada retornada com sucesso.",
    "content": {
      "application/json": {
        "example": {
          "total": 1,
          "items": [{"id": 1, "display_id": "US01", "title": "...", "owner_id": 1}],
          "skip": 0, "limit": 10
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
        "example": {
          "id": 1,
          "display_id": "US01",
          "title": "Título Atualizado",
          "description": "Nova descrição detalhada...",
          "owner_id": 1,
          "created_at": "2025-12-17T15:30:00"
        }
      }
    }
  },
  400: {
    "model": ErrorResponse,
    "description": "Erro de validação: Título já em uso ou campos vazios.",
    "content": {
      "application/json": {
        "examples": {
          "titulo_duplicado": {
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
