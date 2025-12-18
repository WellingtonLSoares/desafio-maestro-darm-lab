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
error_rn_404_example = {
  "model": ErrorResponse,
  "description": "Regra de Negócio não encontrada.",
  "content": {
    "application/json": {
      "example": {"detail": "Regra de Negócio não encontrada"}
    }
  }
}

business_rule_create_responses = {
  201: {
    "model": MessageResponse,
    "description": "Regra de Negócio criada com sucesso.",
    "content": {
      "application/json": {
        "example": {"message": "Regra de Negócio criada com sucesso!"}
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
              "value": {"detail": "Desculpe, o titulo já está em uso"}
            },
            "campos_ausentes": {
              "summary": "Campos obrigatórios",
              "value": {"detail": "O campo 'title' é obrigatório."}
            }
          }
        }
      },
  },
  401: error_401_example
}

business_rule_list_responses = {
  200: {
    "description": "Listagem paginada retornada com sucesso.",
    "content": {
      "application/json": {
        "example": {
          "total": 1,
          "items": [
            {
              "id": 1, 
              "display_id": "RN01", 
              "title": "Cliente deve ser maior de idade", 
              "description": "Para realizar cadastro...",
              "owner_id": 10,
              "created_at": "2025-12-12T10:00:00"
            }
          ],
          "skip": 0, 
          "limit": 5
        }
      }
    }
  },
  401: error_401_example
}

business_rule_update_responses = {
  200: {
    "description": "Regra de Negócio atualizada com sucesso.",
    "content": {
      "application/json": {
        "example": {
          "id": 1,
          "display_id": "RN01",
          "title": "Título Atualizado",
          "description": "Nova descrição...",
          "owner_id": 10,
          "created_at": "2025-12-12T10:00:00"
        }
      }
    }
  },
  400: {
    "model": ErrorResponse,
    "description": "Erro de validação: Título já em uso.",
    "content": {
      "application/json": {
        "examples": {
          "titulo_duplicado": {
            "value": {"detail": "Desculpe, o titulo já está em uso"}
          }
        }
      }
    }
  },
  401: error_401_example,
  404: error_rn_404_example
}

business_rule_delete_responses = {
  200: {
    "model": MessageResponse,
    "description": "Regra de Negócio excluída com sucesso.",
    "content": {
      "application/json": {
        "example": {"message": "Regra de Negócio excluída com sucesso"}
      }
    }
  },
  401: error_401_example,
  404: error_rn_404_example
}