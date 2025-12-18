from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_story_schema import UserStoryCreate, UserStoryResponse, UserStoryPaginatedResponse, UserStoryUpdate
from app.schemas.generic_schema import MessageResponse
from app.services import user_story_service
from app.dependencies import get_current_user
from app.models.users import User
from app.docs.user_story_responses import (
  user_story_create_responses, 
  user_story_list_responses, 
  user_story_delete_responses,
  user_story_update_responses
)
from app.services import association_service
from app.schemas.association_schema import AssociationRequest

router = APIRouter(prefix="/historias", tags=["Histórias de Usuário"])

@router.post(
  "/",
  response_model=UserStoryResponse, 
  status_code=status.HTTP_201_CREATED,
  responses=user_story_create_responses
)
def create_story(
  story: UserStoryCreate, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """
  Cria uma US com título e descrição vinculada a um usuário
  Valida se o título é único
  """
  return user_story_service.create_user_story(db, story, current_user.id)

@router.get(
  "/", 
  response_model=UserStoryPaginatedResponse,
  responses=user_story_list_responses
)
def list_stories(
  db: Session = Depends(get_db), 
  current_user: User = Depends(get_current_user),
  skip: int = 0, 
  limit: int = 10
):
  """
  Lista histórias de usuário com paginação.
  """
  return user_story_service.get_stories_paginated(db, skip=skip, limit=limit)

@router.put(
  "/{story_id}",
  response_model=UserStoryUpdate,
  responses=user_story_update_responses
)
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

@router.delete(
  "/{story_id}", 
  response_model=MessageResponse,
  responses=user_story_delete_responses
)
def delete_story(
  story_id: int, 
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """
  Exclui permanentemente uma história de usuário.
  """
  return user_story_service.delete_user_story(db, story_id, current_user)

@router.post("/{story_id}/associar", status_code=200)
def associate_item_to_story(
  story_id: int, 
  association: AssociationRequest,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return association_service.create_association(
    db, "US", story_id, association, current_user.id
  )

@router.delete("/{story_id}/desassociar", status_code=200)
def remove_association_from_story(
  story_id: int, 
  association: AssociationRequest,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return association_service.delete_association(
    db, "US", story_id, association, current_user.id
  )
