# 📖 Documentação da API

## 📌 Endpoints

### Caminhões (Trucks)

#### `GET /truck`
**Descrição:** Retorna a lista de todos os caminhões cadastrados.

📌 **Exemplo de resposta**
```json
[
  {
    "truck_id": "123e4567-e89b-12d3-a456-426614174000",
    "max_weight": 1000.0
  }
]
```

#### `POST /truck`
**Descrição:** Cadastra um novo caminhão no sistema.

📌 **Corpo da requisição**
```json
{
  "max_weight": 1000.0
}
```

📌 **Exemplo de resposta**
```json
{
  "truck_id": "123e4567-e89b-12d3-a456-426614174000",
  "max_weight": 1000.0
}
```

#### `PUT /truck/{truck_id}`
**Descrição:** Atualiza a capacidade máxima de peso de um caminhão específico.

📌 **Parâmetros da URL**
- `truck_id`: Identificador único do caminhão (UUID)

📌 **Corpo da requisição**
```json
{
  "max_weight": 1200.0
}
```

📌 **Exemplo de resposta**
```json
{
  "truck_id": "123e4567-e89b-12d3-a456-426614174000",
  "max_weight": 1200.0
}
```

### Pedidos (Orders)

#### `GET /order`
**Descrição:** Retorna a lista de todos os pedidos cadastrados.

📌 **Exemplo de resposta**
```json
[
  {
    "order_id": "123e4567-e89b-12d3-a456-426614174000",
    "weight": 500.0,
    "status": "ALLOCATED"
  }
]
```

#### `POST /order`
**Descrição:** Cadastra um novo pedido no sistema.

📌 **Corpo da requisição**
```json
{
  "weight": 500.0
}
```

📌 **Exemplo de resposta**
```json
{
  "order_id": "123e4567-e89b-12d3-a456-426614174000",
  "weight": 500.0,
  "status": "NON_ALLOCATED"
}
```

### Distribuição (Distribution)

#### `GET /distribution`
**Descrição:** Executa o algoritmo de distribuição para alocar pedidos nos caminhões.

📌 **Exemplo de resposta**
```json
{
  "order_distribution": [
    {
      "distribution_id": "123e4567-e89b-12d3-a456-426614174000",
      "order_id": "123e4567-e89b-12d3-a456-426614174001",
      "truck_id": "123e4567-e89b-12d3-a456-426614174002",
      "order_weight": 500.0,
      "truck_max_weight": 1000.0
    }
  ],
  "non_allocated_orders": [
    {
      "non_allocated_order_id": "123e4567-e89b-12d3-a456-426614174003",
      "reason": "Não foi possível alocar o pedido",
      "order_id": "123e4567-e89b-12d3-a456-426614174004"
    }
  ]
}
```

## 📦 Modelos de Dados

### CreateTruckDto
```typescript
{
  max_weight: float  // Capacidade máxima de peso do caminhão
}
```

### UpdateTruckWeightDto
```typescript
{
  max_weight: float  // Nova capacidade máxima de peso do caminhão
}
```

### CreateOrderDto
```typescript
{
  weight: float  // Peso do pedido
}
```

### OrderResponseDTO
```typescript
{
  order_id: UUID    // Identificador único do pedido
  weight: float     // Peso do pedido
  status: OrderStatus  // Status do pedido (ALLOCATED ou NON_ALLOCATED)
}
```

### TruckResponseDTO
```typescript
{
  truck_id: UUID     // Identificador único do caminhão
  max_weight: float  // Capacidade máxima de peso
}
```

### DistributionResponseDTO
```typescript
{
  order_distribution: OrderDistributionResponseDTO[]     // Lista de distribuições realizadas
  non_allocated_orders: NonAllocatedOrderResponseDTO[]   // Lista de pedidos não alocados
}
```

### OrderDistributionResponseDTO
```typescript
{
  distribution_id: UUID    // Identificador único da distribuição
  order_id: UUID          // Identificador do pedido
  truck_id: UUID          // Identificador do caminhão
  order_weight: float     // Peso do pedido
  truck_max_weight: float // Capacidade máxima do caminhão
}
```

### NonAllocatedOrderResponseDTO
```typescript
{
  non_allocated_order_id: UUID  // Identificador do pedido não alocado
  reason: string                // Motivo da não alocação
  order_id: UUID               // Identificador do pedido original
}
```

## 🚦 Códigos de Status

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Parâmetros inválidos na requisição
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## 📝 Observações

- Todos os valores de peso devem ser fornecidos na mesma unidade (ex: quilogramas)
- UUIDs são utilizados como identificadores únicos para todos os recursos
- O algoritmo de distribuição utiliza otimização bin packing para alocar pedidos nos caminhões de forma eficiente
- O status do pedido pode ser:
  - `ALLOCATED`: Pedido alocado em um caminhão
  - `NON_ALLOCATED`: Pedido não alocado