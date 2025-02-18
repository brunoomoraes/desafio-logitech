import pytest

ANY_NAME = "ANY_NAME"
ANY_WEIGHT = 123.456


@pytest.fixture
def item(client):
    response = client.post("/item/", json={"name": ANY_NAME, "weight": ANY_WEIGHT})
    return response.json()


@pytest.mark.parametrize("item_name, weight", [("Item Teste", 100)])
def test_create_item(client, item_name, weight):
    item_json = {"name": item_name, "weight": weight}
    response = client.post("/item/", json=item_json)

    assert response.status_code == 201
    assert response.json()["name"] == item_name
    assert response.json()["weight"] == weight


def test_get_items(client, item):
    item_id = item.get("id")

    response = client.get(f"/item/id/{item_id}")
    assert response.status_code == 200
    assert response.json()
