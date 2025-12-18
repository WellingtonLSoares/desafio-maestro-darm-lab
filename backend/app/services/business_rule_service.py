from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.business_rule import BusinessRule
from app.schemas.business_rule_schema import BusinessRuleCreate
from fastapi import HTTPException
from app.models.item_association import ItemAssociation
from app.services import association_service
from app.utils.type_mapper import get_model_by_type
from app.core.logger import logger

def fetch_items_cache(db: Session, associations: list) -> dict:
  """
  Agrupa IDs por tipo e busca todos os itens no banco de uma vez.
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
  Cruza a associação com o item real do cache para formatar o JSON.
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

def get_rn_response(db: Session, rn: BusinessRule):
  """
  Constrói a resposta completa para UMA Regra de Negócio.
  """
  associations = db.query(ItemAssociation).filter(
    ItemAssociation.source_id == rn.id,
    ItemAssociation.source_type == "RN"
  ).all()

  cache = fetch_items_cache(db, associations)
  formatted_items = serialize_associations(associations, cache)

  return {
    "id": rn.id,
    "display_id": rn.display_id,
    "title": rn.title,
    "description": rn.description,
    "owner_id": rn.owner_id,
    "created_at": rn.created_at,
    "associated_items": formatted_items
  }

def create_rn(db: Session, data: BusinessRuleCreate, user_id: int):
  if db.query(BusinessRule).filter(BusinessRule.title == data.title).first():
    raise HTTPException(status_code=400, detail="Título já existente.")

  new_rn = BusinessRule(
    title=data.title,
    description=data.description,
    owner_id=user_id
  )

  db.add(new_rn)
  db.commit()
  db.refresh(new_rn)

  if data.associations:
    for assoc in data.associations:
      association_service.create_association(
        db, "RN", new_rn.id, assoc, user_id
      )

  return get_rn_response(db, new_rn)

def get_rns_paginated(db: Session, skip: int = 0, limit: int = 5):
  query = db.query(BusinessRule).order_by(desc(BusinessRule.created_at))
  total = query.count()
  items = query.offset(skip).limit(limit).all()

  if not items:
    return {"total": total, "items": [], "skip": skip, "limit": limit}

  rn_ids = [rn.id for rn in items]
  all_associations = db.query(ItemAssociation).filter(
    ItemAssociation.source_type == "RN",
    ItemAssociation.source_id.in_(rn_ids)
  ).all()

  full_cache = fetch_items_cache(db, all_associations)
  
  assoc_map = {}
  for assoc in all_associations:
    assoc_map.setdefault(assoc.source_id, []).append(assoc)

  results = []
  for rn in items:
    rn_assocs = assoc_map.get(rn.id, [])
    formatted_items = serialize_associations(rn_assocs, full_cache)

    results.append({
      "id": rn.id,
      "display_id": rn.display_id,
      "title": rn.title,
      "description": rn.description,
      "owner_id": rn.owner_id,
      "created_at": rn.created_at,
      "associated_items": formatted_items
    })

  return {
    "total": total, 
    "items": results, 
    "skip": skip, 
    "limit": limit
  }

def update_rn(db: Session, rn_id: int, data: BusinessRuleCreate):
  # TODO criar uma classe base para rn e user story, a logica eh msm, inclusive os dados
  db_rn = db.query(BusinessRule).filter(BusinessRule.id == rn_id).first()
  
  if not db_rn:
    raise HTTPException(status_code=404, detail="Regra de Negócio não encontrada")
  
  if data.title != db_rn.title:
    if db.query(BusinessRule).filter(BusinessRule.title == data.title).first():
      raise HTTPException(status_code=400, detail="Desculpe, o titulo já está em uso")

  db_rn.title = data.title
  db_rn.description = data.description
  
  db.commit()
  db.refresh(db_rn)

  return get_rn_response(db, db_rn)

def delete_rn(db: Session, rn_id: int, current_user_id: int):
  db_rn = db.query(BusinessRule).filter(BusinessRule.id == rn_id).first()
  if not db_rn:
    raise HTTPException(status_code=404, detail="Regra de Negócio não encontrada")
  
  logger.info(f"[AUDIT] EXCLUSÃO_RN | User: {current_user_id} | RN_ID: {rn_id} | Título: {db_rn.title}")

  db.query(ItemAssociation).filter(
    ItemAssociation.source_id == rn_id,
    ItemAssociation.source_type == "RN"
  ).delete()

  db.delete(db_rn)
  db.commit()
  
  return {"message": "Regra de Negócio excluída com sucesso"}
