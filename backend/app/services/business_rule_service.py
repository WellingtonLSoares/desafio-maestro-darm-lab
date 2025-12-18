from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.business_rule import BusinessRule
from app.schemas.business_rule_schema import BusinessRuleCreate
from fastapi import HTTPException

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

  return new_rn

def get_rns_paginated(db: Session, skip: int = 0, limit: int = 5):
  query = db.query(BusinessRule).order_by(desc(BusinessRule.created_at))
  total = query.count()
  items = query.offset(skip).limit(limit).all()

  return {
    "total": total, 
    "items": items, 
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

  return db_rn

def delete_rn(db: Session, rn_id: int):
  db_rn = db.query(BusinessRule).filter(BusinessRule.id == rn_id).first()
  if not db_rn:
    raise HTTPException(status_code=404, detail="Regra de Negócio não encontrada")
  
  db.delete(db_rn)
  db.commit()
  
  return {"message": "Regra de Negócio excluída com sucesso"}
