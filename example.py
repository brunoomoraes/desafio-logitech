import requests

main_url = "http://127.0.0.1:8000/"


def exec_items(main_url):
    url = f"{main_url}/item/"
    data = {"name": "Monitor 27'", "weight": 1500.75}

    print("Criando os itens")
    for _ in range(1, 4):
        final_url = f"{url}"
        response = requests.post(final_url, json=data)
        print(response.json())  # Mostra a resposta da API

    print("Listando todos os itens")
    response = requests.get(f"{url}all")
    print(response.json())
    total_items = response.json().get("items")
    total = len(total_items)
    # print(total)

    print("Pegando cada item")
    for i in range(1, 5):
        final_url = f"{url}id/{i}"
        response = requests.get(final_url)
        print(response.json())

    print("Removendo cada item")
    for item in total_items:
        final_url = f"{url}id/{item.get('id')}"
        response = requests.delete(final_url)
        print(response.json())

    print("Listando todos os itens")
    response = requests.get(f"{url}all")
    print(response.json())


def exec_truck(main_url):
    url = f"{main_url}/truck/"
    data = {"name": "Geraldo", "weight_max": 50000000}

    print("Criando os caminhões")
    for _ in range(1, 4):
        final_url = f"{url}"
        response = requests.post(final_url, json=data)
        print(response.json())  # Mostra a resposta da API

    print("Listando todos os caminhões")
    response = requests.get(f"{url}all")
    print(response.json())
    total_trucks = response.json().get("trucks")
    total = len(total_trucks)
    # print(total)

    print("Pegando cada caminhão")
    for i in range(1, 5):
        final_url = f"{url}id/{i}"
        response = requests.get(final_url)
        print(response.json())

    print("Removendo cada caminhão")
    for truck in total_trucks:
        final_url = f"{url}id/{truck.get('id')}"
        response = requests.delete(final_url)
        print(response.json())

    print("Listando todos os caminhões")
    response = requests.get(f"{url}all")
    print(response.json())


def exec_distruicao(main_url):
    truck_url = f"{main_url}truck/"
    item_url = f"{main_url}item/"
    distruicao_url = f"{main_url}distribuir"

    # add trucks
    trucks = [
        {"name": "Truck Azul", "weight_max": 10},
        {"name": "Truck Vermelho", "weight_max": 15},
    ]

    for truck in trucks:
        requests.post(truck_url, json=truck)

    # add items
    items = [
        {"name": "Caixa de ferramenta", "weight": 2},
        {"name": "Motor Peças", "weight": 3},
        {"name": "Bobina de cobre", "weight": 2.5},
        {"name": "Palete de Madeira", "weight": 2.5},
        {"name": "Compressor de Ar", "weight": 5},
        {"name": "Tanque de Óleo", "weight": 3},
        {"name": "Barril de Produtos", "weight": 2},
        {"name": "Geração de Energia", "weight": 2.5},
        {"name": "Conjunto de Rodas", "weight": 1.5},
        {"name": "Painel Solar", "weight": 1},
    ]
    for item in items:
        requests.post(item_url, json=item)

    # Execute distruition
    print(requests.get(distruicao_url).json())

    # print result
    print("Listando todos os caminhões")
    response = requests.get(f"{truck_url}all")
    print(response.json())
    print("Listando todos os caminhões")
    response = requests.get(f"{item_url}all")
    print(response.json())


if __name__ == "__main__":
    exec_items(main_url)
    # exec_truck(main_url)
    # exec_distruicao(main_url)
