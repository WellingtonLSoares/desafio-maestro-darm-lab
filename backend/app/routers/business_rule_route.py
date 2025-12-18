from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.business_rule_schema import BusinessRuleResponse, BusinessRulePaginatedResponse, BusinessRuleCreate
from app.services import business_rule_service
from app.docs.business_rule_responses import (
  business_rule_create_responses,
  business_rule_list_responses,
  business_rule_update_responses,
  business_rule_delete_responses
)

router = APIRouter(prefix="/regras-negocio", tags=["Regras de Negócio"])

@router.post(
  "/",
  response_model=BusinessRuleResponse, 
  responses=  business_rule_create_responses,

)
def create(
  rn: BusinessRuleCreate, 
  db: Session = Depends(get_db), 
  user = Depends(get_current_user)
):
  return business_rule_service.create_rn(db, rn, user.id)

@router.get(
  "/", 
  response_model=BusinessRulePaginatedResponse,
  responses=business_rule_list_responses
)
def list_all(
  skip: int = 0, 
  limit: int = 5, 
  db: Session = Depends(get_db), 
  user = Depends(get_current_user)
):
  return business_rule_service.get_rns_paginated(db, skip, limit)

@router.put(
  "/{rn_id}", 
  response_model=BusinessRuleResponse,
  responses=business_rule_update_responses
)
def update(rn_id: int, rn: BusinessRuleCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
  return business_rule_service.update_rn(db, rn_id, rn)
