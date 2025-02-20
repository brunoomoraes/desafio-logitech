from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Truck
from backend.schemas import TruckCreate, TruckListResponse, TruckResponse

router = APIRouter()


@router.post("/", response_model=TruckResponse, status_code=201)
def create_new_truck(truck: TruckCreate, db: Session = Depends(get_db)):
    print(truck)
    db_truck = Truck(name=truck.name, weight_max=truck.weight_max)
    db.add(db_truck)
    db.commit()
    db.refresh(db_truck)
    return db_truck


@router.get("/all/", response_model=TruckListResponse)
def get_all_truck(db: Session = Depends(get_db)):
    trucks = db.query(Truck).all()

    return {"trucks": trucks}


@router.get("/id/{truck_id}", response_model=TruckResponse)
def get_truck(truck_id: int, db: Session = Depends(get_db)):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()
    if not truck:
        raise HTTPException(status_code=404, detail="Caminhão não encontrado")
    return truck


@router.delete("/id/{truck_id}")
def delete_truck(truck_id: int, db: Session = Depends(get_db)):
    truck = db.query(Truck).filter(Truck.id == truck_id).first()
    if not truck:
        raise HTTPException(status_code=404, detail="Caminhão não encontrado")
    db.delete(truck)
    db.commit()
    return {"message": "Caminhão removido com sucesso"}
