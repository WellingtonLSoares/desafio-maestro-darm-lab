from sqlalchemy.orm import Session, load_only
from app.models.user_story import UserStory
from app.schemas.user_story_schema import UserStoryCreate
from fastapi import HTTPException, status
from sqlalchemy import and_, desc
from app.models.item_association import ItemAssociation
from app.core import logger
from app.services import association_service
from app.utils.type_mapper import get_model_by_type

def fetch_items_cache(db: Session, associations: list) -> dict:
  """
  Recebe uma lista de associações, agrupa por tipo(RN),
  busca todos os itens reais no banco de uma vez
  e retorna um dicionário.
  
  Retorno: {'RN': {1: ObjetoRN, 2: ObjetoRN}, 'RF': {...}}
  """
  if not associations:
    return {}

  ids_by_type = {}
  for assoc in associations:
    ids_by_type.setdefault(assoc.target_type, set()).add(assoc.target_id)

  items_cache = {}
  for item_type, ids in ids_by_type.items():
    model = get_model_by_type(item_type)

    if model:
      found_items = db.query(model).filter(model.id.in_(ids)).all()
      items_cache[item_type] = {item.id: item for item in found_items}
  
  return items_cache

def serialize_associations(associations: list, items_cache: dict) -> list:
  """
  Formata a lista final para o JSON, cruzando a associação com o item real do cache.
  """
  result = []
  for assoc in associations:
    type_cache = items_cache.get(assoc.target_type, {})
    item = type_cache.get(assoc.target_id)

    if item:
      result.append({
        "type": assoc.target_type,
        "id": assoc.target_id,
        "display_id": item.display_id,
        "title": item.title
      })

  return result

def get_story_response(db: Session, story: UserStory):
  """
  Constrói a resposta completa para UMA história (usado no Create/Update).
  """
  associations = db.query(ItemAssociation).filter(
    ItemAssociation.source_id == story.id,
    ItemAssociation.source_type == "US"
  ).all()

  cache = fetch_items_cache(db, associations)
  formatted_items = serialize_associations(associations, cache)

  return {
    "id": story.id,
    "display_id": story.display_id,
    "title": story.title,
    "description": story.description,
    "owner_id": story.owner_id,
    "created_at": story.created_at,
    "associated_items": formatted_items
  }

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

  return get_story_response(db, new_story)

def get_stories_paginated(db: Session, skip: int = 0, limit: int = 10):
  query = db.query(UserStory).order_by(UserStory.created_at.desc())
  total = query.count()
  stories = query.offset(skip).limit(limit).all()

  story_ids = [s.id for s in stories]

  associations = db.query(ItemAssociation).filter(
    ItemAssociation.source_type == "US",
    ItemAssociation.source_id.in_(story_ids)
  ).all()

  full_cache = fetch_items_cache(db, associations)

  results = []

  assoc_map = {}
  for assoc in associations:
    assoc_map.setdefault(assoc.source_id, []).append(assoc)

  for story in stories:
    story_assocs = assoc_map.get(story.id, [])
    formatted_items = serialize_associations(story_assocs, full_cache)

    results.append({
      "id": story.id,
      "display_id": story.display_id,
      "title": story.title,
      "description": story.description,
      "owner_id": story.owner_id,
      "created_at": story.created_at,
      "associated_items": formatted_items
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

  return get_story_response(db, db_story)

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
