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
