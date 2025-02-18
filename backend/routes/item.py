from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.schemas import ItemCreate, ItemResponse, ItemListResponse
from backend.database import get_db
from backend.models import Item

router = APIRouter()


@router.post("/", response_model=ItemResponse, status_code=201)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, weight=item.weight)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/all/", response_model=ItemListResponse)
def get_all_item(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return {"items": items}


@router.get("/id/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@router.delete("/id/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(item)
    db.commit()
    return {"message": "Item removido com sucesso"}
