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
