from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user_story_schema import UserStoryCreate, UserStoryResponse, UserStoryPaginatedResponse
from app.schemas.generic_schema import MessageResponse
from app.services import user_story_service
from app.dependencies import get_current_user
from app.models.users import User

router = APIRouter(prefix="/historias", tags=["Histórias de Usuário"])

@router.post("/", response_model=UserStoryResponse, status_code=status.HTTP_201_CREATED)
def create_story(
  story: UserStoryCreate, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return user_story_service.create_user_story(db, story, current_user.id)

@router.get("/", response_model=UserStoryPaginatedResponse)
def list_stories(
  db: Session = Depends(get_db), 
  current_user: User = Depends(get_current_user),
  skip: int = 0, 
  limit: int = 10
):
  """
  Lista histórias de usuário com paginação para a visualização em tabela.
  🔒 Exige Autenticação.
  """
  return user_story_service.get_stories_paginated(db, skip=skip, limit=limit)

@router.put("/{story_id}", response_model=UserStoryResponse)
def update_story(
  story_id: int, 
  story: UserStoryCreate, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """
  Edita uma história existente.
  """
  return user_story_service.update_user_story(db, story_id, story)

# EXCLUIR
@router.delete("/{story_id}", response_model=MessageResponse)
def delete_story(
  story_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """
  Exclui permanentemente uma história de usuário.
  """
  return user_story_service.delete_user_story(db, story_id)
