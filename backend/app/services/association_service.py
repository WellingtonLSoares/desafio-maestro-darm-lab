from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.item_association import ItemAssociation
from app.utils.type_mapper import get_model_by_type
from app.schemas.association_schema import AssociationRequest
from app.core.logger import logger

def validate_item_exists(db: Session, item_type: str, item_id: int):
  """Verifica se o item existe na tabela correspondente."""
  model = get_model_by_type(item_type)
  if not model:
    raise HTTPException(status_code=400, detail=f"Tipo de item '{item_type}' inválido.")
  
  item = db.query(model).filter(model.id == item_id).first()

  if not item:
    raise HTTPException(status_code=404, detail=f"{item_type} com ID {item_id} não encontrado.")

def create_association(db: Session, source_type: str, source_id: int, target_data: AssociationRequest, user_id: int):
  validate_item_exists(db, source_type, source_id)
  validate_item_exists(db, target_data.item_type, target_data.item_id)

  if source_type == target_data.item_type and source_id == target_data.item_id:
    raise HTTPException(status_code=400, detail="Um item não pode ser associado a si mesmo.")

  if source_type == "US" and target_data.item_type == "US":
    raise HTTPException(status_code=400, detail="Uma História de Usuário não pode ser associada a outra História.")
  
  existing_link = db.query(ItemAssociation).filter(
    ItemAssociation.target_id == target_data.item_id,
    ItemAssociation.target_type == target_data.item_type,
    ItemAssociation.source_type == source_type # Se já tem vínculo com alguma US
  ).first()

  if existing_link:
    if existing_link.source_id != source_id:
      raise HTTPException(status_code=400, detail="Item já associado.")
    
    return {"message": "Item já associado."}

  new_assoc = ItemAssociation(
    source_id=source_id,
    source_type=source_type,
    target_id=target_data.item_id,
    target_type=target_data.item_type
  )
  db.add(new_assoc)
  db.commit()

  logger.info(f"[AUDIT] ASSOCIAR | User: {user_id} | {source_type}:{source_id} -> {target_data.item_type}:{target_data.item_id}")
  
  return {"message": "Item associado com sucesso."}

def delete_association(db: Session, source_type: str, source_id: int, target_data: AssociationRequest, user_id: int):
  # Busca a associação específica
  assoc = db.query(ItemAssociation).filter(
    ItemAssociation.source_id == source_id,
    ItemAssociation.source_type == source_type,
    ItemAssociation.target_id == target_data.item_id,
    ItemAssociation.target_type == target_data.item_type
  ).first()

  if not assoc:
    raise HTTPException(status_code=404, detail="Associação não encontrada.")

  db.delete(assoc)
  db.commit()

  logger.info(f"[AUDIT] REMOVER | User: {user_id} | {source_type}:{source_id} X {target_data.item_type}:{target_data.item_id}")

  return {"message": "Associação removida com sucesso."}
