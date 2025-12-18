from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.business_rule_schema import BusinessRuleResponse, BusinessRulePaginatedResponse, BusinessRuleCreate, BusinessRuleUpdate
from app.services import business_rule_service
from app.docs.business_rule_responses import (
  business_rule_create_responses,
  business_rule_list_responses,
  business_rule_update_responses,
  business_rule_delete_responses
)
from app.models.users import User
from app.schemas.association_schema import AssociationRequest
from app.services import association_service

router = APIRouter(prefix="/regras-negocio", tags=["Regras de Negócio"])

@router.post(
  "/",
  response_model=BusinessRuleResponse, 
  responses=business_rule_create_responses,
  status_code=status.HTTP_201_CREATED
)
def create(
  rn: BusinessRuleCreate, 
  db: Session = Depends(get_db), 
  user: User = Depends(get_current_user)
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
  user: User = Depends(get_current_user)
):
  return business_rule_service.get_rns_paginated(db, skip, limit)

@router.put(
  "/{rn_id}", 
  response_model=BusinessRuleUpdate,
  responses=business_rule_update_responses
)
def update(rn_id: int, rn: BusinessRuleCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
  return business_rule_service.update_rn(db, rn_id, rn)

@router.delete("/{rn_id}", responses=business_rule_delete_responses)
def delete(rn_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
  return business_rule_service.delete_rn(db, rn_id, user.id)

@router.post("/{rn_id}/associar", status_code=200)
def associate_item_to_rn(
  rn_id: int, 
  association: AssociationRequest,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """
  Associa um item (US, RN) à Regra de Negócio.
  Valida Item já associado e Auto-associação.
  """
  return association_service.create_association(
    db, "RN", rn_id, association, current_user.id
  )

@router.delete("/{rn_id}/desassociar", status_code=200)
def remove_association_from_rn(
  rn_id: int, 
  association: AssociationRequest,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """
  Remove uma associação existente (RN019).
  """
  return association_service.delete_association(
    db, "RN", rn_id, association, current_user.id
  )
