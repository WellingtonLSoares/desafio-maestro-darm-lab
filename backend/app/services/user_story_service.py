from sqlalchemy.orm import Session, load_only
from app.models.user_story import UserStory
from app.schemas.user_story_schema import UserStoryCreate
from fastapi import HTTPException, status
from sqlalchemy import and_

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
    parent_id=story_data.parent_id,
    owner_id=current_user_id
  )

  db.add(new_story)
  db.commit()
  db.refresh(new_story)

  return new_story

def get_stories_paginated(db: Session, skip: int = 0, limit: int = 10):
  """
  Retorna as histórias de forma paginada.
  """
  query = db.query(UserStory)
  
  total = query.count()
  items = query.offset(skip).limit(limit).all()
  
  return {
    "total": total,
    "items": items,
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
  db_story.parent_id = story_data.parent_id

  db.commit()
  db.refresh(db_story)

  return db_story

def delete_user_story(db: Session, story_id: int):
  """
  Remove a história do sistema.
  """
  db_story = db.query(UserStory).filter(UserStory.id == story_id).first()
  
  # add validacao de usuario? us nao menciona esse tipo de coisa, dando a entender acesso geral, bastando estar logado

  if not db_story:
    raise HTTPException(status_code=404, detail="História de usuário não encontrada.")

  db.delete(db_story)
  db.commit()

  return {"message": "História excluída com sucesso."}
