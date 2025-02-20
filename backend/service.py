from typing import List, Tuple

from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Item, Truck


def distribuir_pedidos():
    db: Session = next(get_db())

    trucks = db.query(Truck).all()
    items = db.query(Item).all()

    items = _sort_item(items)

    for truck in trucks:
        list_items_id, items = _add_items_in_truck(truck, items)

        for item_id in list_items_id:
            db_item = db.query(Item).filter(Item.id == item_id).first()
            db_item.truck_id = truck.id
            db.commit()

    return {"mensagem": "Distribuição realizada"}


def _add_items_in_truck(truck: Truck, items: List[Item]) -> Tuple[List[int], List[Item]]:
    pos_item = 0
    list_items_id = []
    while pos_item < len(items) and truck.can_receive_more_items():
        item = items[pos_item]
        if truck.can_add_item(item):
            truck.weight_current += item.weight
            truck.items.append(item)
            list_items_id.append(item.id)
            items.pop(pos_item)
        else:
            pos_item += 1

    return (list_items_id, items)


def _sort_item(items: List[Item]) -> List[Item]:
    if not items:
        return []

    new_list = [items[0]]
    pos_item = 0
    for element in items[1:]:
        while pos_item < len(new_list):
            if element.weight > new_list[pos_item].weight:
                new_list.insert(pos_item, element)
                break
            else:
                pos_item += 1

        if pos_item == len(new_list):
            new_list.append(element)

    return new_list
