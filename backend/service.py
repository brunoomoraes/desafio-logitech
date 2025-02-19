from sqlalchemy.orm import Session

from backend.models import Item, Truck

from typing import List, Tuple


def distribuir_pedidos(db: Session):
    # Lógica para otimizar carga nos caminhões
    trucks = db.query(Truck).all()
    items = list(db.query(Item).all())
    print(items)

    items = _sorte_item(items)

    for truck in trucks:
        print(f"Ajustando Truck {truck.id}")
        list_items_id, items = _add_items_in_truck(truck, items)
        print(f"Itens que devem ser adicionados nesse caminhão : {list_items_id}")
        print("\n" * 2)
        print(items)
        print("\n" * 2)
        for item_id in list_items_id:
            print(f"Item Id: {item_id}")
            db_item = db.query(Item).filter(Item.id == item_id).first()
            db_item.truck_id = truck.id
            db.commit()

    return {"mensagem": "Distribuição realizada"}


def _add_items_in_truck(truck: Truck, items: List[Item]) -> Tuple[List[int], List[Item]]:
    pos_item = 0
    list_items_id = []
    # print("Adicionando items no caminhão {truck.id}")
    while pos_item < len(items) and truck.can_receive_more_items():
        # print("="*100)
        # print(f"Postion: {pos_item}")
        # print(f"Items: {items}")
        item = items[pos_item]
        # print(f"Postion: {item}")
        # print("="*100)
        if truck.can_add_item(item):
            print(f"{truck.weight_current} + {item.weight} <= {truck.weight_max}")
            truck.weight_current += item.weight
            truck.items.append(item)
            list_items_id.append(item.id)
            items.pop(pos_item)
        else:
            pos_item += 1

    return (list_items_id, items)


def _sorte_item(items: List[Item]) -> List[Item]:
    new_list = []
    for element in items:
        new_list.append(element)
    new_list.sort(key=lambda item: -item.weight)
    return new_list
