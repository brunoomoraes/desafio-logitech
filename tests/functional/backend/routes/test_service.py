import pytest

from backend.database import get_db
from backend.models import Item, Truck

db = next(get_db())

ANY_NAME = "ANY_NAME"
ANY_WEIGHT = 123.456


@pytest.fixture
def mock_truck_list(truck_list):
    db_truck_list = []
    for truck in truck_list:
        db_truck = Truck(name=truck["name"], weight_max=truck["weight_max"])
        db.add(db_truck)
        db.commit()
        db.refresh(db_truck)
        db_truck_list.append(db_truck)
    return db_truck_list


@pytest.fixture
def mock_item_list(item_list, test_db):
    db_item_list = []
    for item in item_list:
        db_item = Item(name=item["name"], weight=item["weight"], truck_id=None)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        db_item_list.append(db_item)
    return db_item_list


@pytest.mark.parametrize(
    "item_list, truck_list, expected_truck_item_relation",
    [
        (
            [
                {"name": "Caixa de ferramenta", "weight": 2},  # 1
                {"name": "Motor Peças", "weight": 3},  # 2
                {"name": "Bobina de cobre", "weight": 2.5},  # 3
                {"name": "Palete de Madeira", "weight": 2.5},  # 4
                {"name": "Compressor de Ar", "weight": 5},  # 5
                {"name": "Tanque de Óleo", "weight": 3},  # 6
                {"name": "Barril de Produtos", "weight": 2},  # 7
                {"name": "Geração de Energia", "weight": 2.5},  # 8
                {"name": "Conjunto de Rodas", "weight": 1.5},  # 9
                {"name": "Painel Solar", "weight": 1},  # 10
            ],
            [
                {"name": "Truck Azul", "weight_max": 10},  # 1
                {"name": "Truck Vermelho", "weight_max": 15},  # 2
            ],
            (
                (1, 2),
                (2, 1),
                (3, 1),
                (4, 2),
                (5, 2),
                (6, 1),
                (7, 2),
                (8, 2),
                (9, 1),
                (10, 2),
            ),
        ),
        (
            [
                {"name": "Caixa de ferramenta", "weight": 2},  # 1
                {"name": "Motor Peças", "weight": 3},  # 2
                {"name": "Bobina de cobre", "weight": 2.5},  # 3
                {"name": "Palete de Madeira", "weight": 2.5},  # 4
                {"name": "Compressor de Ar", "weight": 5},  # 5
                {"name": "Tanque de Óleo", "weight": 3},  # 6
                {"name": "Barril de Produtos", "weight": 2},  # 7
                {"name": "Geração de Energia", "weight": 2.5},  # 8
                {"name": "Conjunto de Rodas", "weight": 1.5},  # 9
                {"name": "Painel Solar", "weight": 1},  # 10
                {"name": "Computador", "weight": 20},  # 11
            ],
            [
                {"name": "Truck Azul", "weight_max": 10},  # 1
                {"name": "Truck Vermelho", "weight_max": 15},  # 2
            ],
            (
                (1, 2),
                (2, 1),
                (3, 1),
                (4, 2),
                (5, 2),
                (6, 1),
                (7, 2),
                (8, 2),
                (9, 1),
                (10, 2),
                (11, None),
            ),
        ),
        (
            [],
            [
                {"name": "Truck Azul", "weight_max": 10},  # 1
                {"name": "Truck Vermelho", "weight_max": 15},  # 2
            ],
            (),
        ),
    ],
)
def test_service_distribuir(
    client,
    item_list,
    truck_list,
    expected_truck_item_relation,
    mock_item_list,
    mock_truck_list,
):
    client.get("/distribuir")

    for item_id, truck_id in expected_truck_item_relation:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        assert db_item.truck_id == truck_id
