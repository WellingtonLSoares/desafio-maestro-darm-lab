from sqlalchemy.orm import Session, load_only
from app.models.user_story import UserStory
from app.schemas.user_story_schema import UserStoryCreate
from fastapi import HTTPException, status
from sqlalchemy import and_, desc
from app.models.item_association import ItemAssociation
from app.core import logger
from app.services import association_service
from app.utils.type_mapper import get_model_by_type

def create_user_story(db: Session, story_data: UserStoryCreate, current_user_id: int):
  db_story = db.query(UserStory).filter(UserStory.title == story_data.title).options(
    load_only(
      UserStory.id,
      UserStory.title
    )
  ).first()

  if db_story:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="O título já está em uso."
    )

  new_story = UserStory(
    title=story_data.title,
    description=story_data.description,
    owner_id=current_user_id
  )
  
  db.add(new_story)
  db.commit()
  db.refresh(new_story)

  if story_data.associations:
    for assoc in story_data.associations:
      association_service.create_association(
        db,
        "US",
        new_story.id,
        assoc,
        current_user_id
      )

  return new_story

def get_stories_paginated(db: Session, skip: int = 0, limit: int = 10):
  query = db.query(UserStory).order_by(UserStory.created_at.desc())

  total = query.count()
  stories = query.offset(skip).limit(limit).all()

  story_ids = [s.id for s in stories]

  associations = db.query(ItemAssociation).filter(
    ItemAssociation.source_type == "US",
    ItemAssociation.source_id.in_(story_ids)
  ).all()

  assoc_map = {}
  for assoc in associations:
    assoc_map.setdefault(assoc.source_id, []).append(assoc)

  results = []

  for story in stories:
    associated_data = []

    for assoc in assoc_map.get(story.id, []):
      model = get_model_by_type(assoc.target_type)
      
      if not model:
        continue

      target_item = db.query(model).filter(model.id == assoc.target_id).first()
      if not target_item:
        continue

      associated_data.append({
        "type": assoc.target_type,
        "id": assoc.target_id,
        "display_id": target_item.display_id,
        "title": target_item.title
      })

    results.append({
      "id": story.id,
      "display_id": story.display_id,
      "title": story.title,
      "description": story.description,
      "owner_id": story.owner_id,
      "created_at": story.created_at,
      "associated_items": associated_data
    })

  return {
    "total": total,
    "items": results,
    "skip": skip,
    "limit": limit
  }

def update_user_story(db: Session, story_id: int, story_data: UserStoryCreate):
  """
  Permite editar título e descrição.
  Valida unicidade do título se for alterado.
  """
  db_story = db.query(UserStory).filter(UserStory.id == story_id).first()
  
  # add validacao de usuario? us nao menciona esse tipo de coisa, dando a entender acesso geral, bastando estar logado

  if not db_story:
    raise HTTPException(status_code=404, detail="História de usuário não encontrada.")

  if story_data.title != db_story.title:
    title_exists = db.query(UserStory).filter(
      and_(UserStory.title == story_data.title, UserStory.id != story_id)
    ).first()

    if title_exists:
      raise HTTPException(status_code=400, detail="O título já está em uso.")

  db_story.title = story_data.title
  db_story.description = story_data.description

  db.commit()
  db.refresh(db_story)

  return db_story

def delete_user_story(db: Session, story_id: int, current_user_id: int):
  """
  Remove a história do sistema.
  """
  db_story = db.query(UserStory).filter(UserStory.id == story_id).first()
  
  # add validacao de usuario? us nao menciona esse tipo de coisa, dando a entender acesso geral, bastando estar logado

  if not db_story:
    raise HTTPException(status_code=404, detail="História de usuário não encontrada.")

  logger.info(f"[AUDIT] EXCLUSÃO_HISTORIA | User: {current_user_id} | US_ID: {story_id} | Título: {db_story.title}")

  db.query(ItemAssociation).filter(
    ItemAssociation.source_id == story_id,
    ItemAssociation.source_type == "US"
  ).delete()

  db.delete(db_story)
  db.commit()

  return {"message": "História excluída com sucesso."}
