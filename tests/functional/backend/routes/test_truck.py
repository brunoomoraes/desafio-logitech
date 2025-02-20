import pytest

from backend.database import get_db
from backend.models import Truck

db = next(get_db())

ANY_NAME = "ANY_NAME"
ANY_WEIGHT = 123.456


@pytest.fixture
def truck(client):
    db_truck = Truck(name=ANY_NAME, weight_max=ANY_WEIGHT)
    db.add(db_truck)
    db.commit()
    db.refresh(db_truck)
    return db_truck


@pytest.fixture
def truck_list(client, number_trucks):
    truck_list = []
    for i in range(number_trucks):
        db_truck = Truck(name=f"{ANY_NAME} {i}", weight_max=ANY_WEIGHT)
        db.add(db_truck)
        db.commit()
        db.refresh(db_truck)
        truck_list.append(db_truck)
    return truck_list


@pytest.mark.parametrize("truck_name, weight_max", [("Truck Teste", 100)])
def test_create_truck(client, truck_name, weight_max):
    truck_json = {"name": truck_name, "weight_max": weight_max}

    response = client.post("/truck/", json=truck_json)
    truck = response.json()

    assert response.status_code == 201
    assert truck["name"] == truck_name
    assert truck["weight_max"] == weight_max


def test_get_truck(client, truck):
    response = client.get(f"/truck/id/{truck.id}")

    assert response.status_code == 200
    assert response.json()


@pytest.mark.parametrize("number_trucks", [0, 2, 5])
def test_get_all_trucks(client, number_trucks, truck_list):
    response = client.get("/truck/all/")
    trucks = response.json().get("trucks")

    assert response.status_code == 200
    assert len(trucks) == number_trucks

    for truck in truck_list:
        truck_format = {
            "id": truck.id,
            "name": truck.name,
            "weight_max": truck.weight_max,
            "weight_current": 0,
            "items": [],
        }
        trucks.remove(truck_format)

    assert trucks == []


def test_delete_truck(client, truck):
    response = client.delete(f"/truck/id/{truck.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Caminhão removido com sucesso"


def test_get_truck_not_found(client):
    response = client.get("/truck/id/0")

    assert response.status_code == 404
    assert response.json()["detail"] == "Caminhão não encontrado"


def test_delete_truck_not_found(client):
    response = client.delete("/truck/id/0")

    assert response.status_code == 404
    assert response.json()["detail"] == "Caminhão não encontrado"
