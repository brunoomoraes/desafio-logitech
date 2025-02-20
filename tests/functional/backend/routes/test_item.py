import pytest

from backend.database import get_db
from backend.models import Item

db = next(get_db())

ANY_NAME = "ANY_NAME"
ANY_WEIGHT = 123.456


@pytest.fixture
def item(client):
    db_item = Item(name=ANY_NAME, weight=ANY_WEIGHT)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@pytest.fixture
def item_list(client, number_items):
    item_list = []
    for i in range(number_items):
        db_item = Item(name=f"{ANY_NAME} {i}", weight=ANY_WEIGHT)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        item_list.append(db_item)
    return item_list


@pytest.mark.parametrize("item_name, weight", [("Item Teste", 100)])
def test_create_item(client, item_name, weight):
    item_json = {"name": item_name, "weight": weight}

    response = client.post("/item/", json=item_json)
    item = response.json()

    assert response.status_code == 201
    assert item["name"] == item_name
    assert item["weight"] == weight


def test_get_item(client, item):
    response = client.get(f"/item/id/{item.id}")

    assert response.status_code == 200
    assert response.json()


@pytest.mark.parametrize("number_items", [0, 2, 5])
def test_get_all_items(client, number_items, item_list):
    response = client.get("/item/all/")
    items = response.json().get("items")

    assert response.status_code == 200
    assert len(items) == number_items

    for item in item_list:
        item_format = {"id": item.id, "name": item.name, "weight": item.weight}
        items.remove(item_format)

    assert items == []


def test_delete_item(client, item):
    response = client.delete(f"/item/id/{item.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Item removido com sucesso"


def test_get_item_not_found(client):
    response = client.get("/item/id/0")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item não encontrado"


def test_delete_item_not_found(client):
    response = client.delete("/item/id/0")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item não encontrado"
