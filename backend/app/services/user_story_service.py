from sqlalchemy.orm import Session, load_only
from app.models.user_story import UserStory
from app.schemas.user_story_schema import UserStoryCreate
from fastapi import HTTPException, status

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
  Retorna as histórias de forma paginada para popular a tabela do Figma.
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
