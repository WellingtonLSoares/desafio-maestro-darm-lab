from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from app.models.business_rule import BusinessRule
from app.schemas.business_rule_schema import BusinessRuleCreate
from fastapi import HTTPException
from app.models.item_association import ItemAssociation
from app.services import association_service
from app.utils.type_mapper import get_model_by_type
from app.core.logger import logger

def fetch_items_cache_bidirectional(db: Session, items_to_fetch: list) -> dict:
  """
  Agrupa IDs por tipo e busca todos os itens no banco de uma vez.
  """
  if not items_to_fetch:
    return {}

  ids_by_type = {}
  for item_type, item_id in items_to_fetch:
    ids_by_type.setdefault(item_type, set()).add(item_id)

  items_cache = {}
  for item_type, ids in ids_by_type.items():
    model = get_model_by_type(item_type)
    if model:
      found_items = db.query(model).filter(model.id.in_(ids)).all()
      items_cache[item_type] = {item.id: item for item in found_items}

  return items_cache

def get_rn_response(db: Session, rn: BusinessRule):
  """
  Constrói a resposta completa para UMA Regra de Negócio.
  """
  associations = db.query(ItemAssociation).filter(
    or_(
      and_(ItemAssociation.source_type == "RN", ItemAssociation.source_id == rn.id),
      and_(ItemAssociation.target_type == "RN", ItemAssociation.target_id == rn.id)
    )
  ).all()

  items_to_fetch = []
  normalized_assocs = []

  for assoc in associations:
    if assoc.source_type == "RN" and assoc.source_id == rn.id:
      p_type, p_id = assoc.target_type, assoc.target_id
    else:
      p_type, p_id = assoc.source_type, assoc.source_id
    
    items_to_fetch.append((p_type, p_id))
    normalized_assocs.append({'type': p_type, 'id': p_id})

  cache = fetch_items_cache_bidirectional(db, items_to_fetch)
  
  formatted_items = []
  for item_info in normalized_assocs:
    type_cache = cache.get(item_info['type'], {})
    item_obj = type_cache.get(item_info['id'])
    
    if item_obj:
      formatted_items.append({
        "type": item_info['type'],
        "id": item_info['id'],
        "display_id": item_obj.display_id,
        "title": item_obj.title
      })

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
    or_(
      and_(ItemAssociation.source_type == "RN", ItemAssociation.source_id.in_(rn_ids)),
      and_(ItemAssociation.target_type == "RN", ItemAssociation.target_id.in_(rn_ids))
    )
  ).all()
  
  assoc_map = {} 
  all_partners_to_fetch = []

  for assoc in all_associations:
    if assoc.source_type == "RN" and assoc.source_id in rn_ids:
      my_rn_id = assoc.source_id
      partner_type = assoc.target_type
      partner_id = assoc.target_id

    else:
      my_rn_id = assoc.target_id
      partner_type = assoc.source_type
      partner_id = assoc.source_id

    pair = (partner_type, partner_id)
    all_partners_to_fetch.append(pair)
    
    assoc_map.setdefault(my_rn_id, []).append(pair)

  full_cache = fetch_items_cache_bidirectional(db, all_partners_to_fetch)
  
  results = []
  for rn in items:
    my_partners = assoc_map.get(rn.id, [])
    formatted_items = []

    for p_type, p_id in my_partners:
      type_cache = full_cache.get(p_type, {})
      item_obj = type_cache.get(p_id)

      if item_obj:
        formatted_items.append({
          "type": p_type,
          "id": p_id,
          "display_id": item_obj.display_id,
          "title": item_obj.title
        })

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
    or_(
      and_(ItemAssociation.source_type == "RN", ItemAssociation.source_id == rn_id),
      and_(ItemAssociation.target_type == "RN", ItemAssociation.target_id == rn_id)
    )
  ).delete(synchronize_session=False)

  db.delete(db_rn)
  db.commit()
  
  return {"message": "Regra de Negócio excluída com sucesso"}
