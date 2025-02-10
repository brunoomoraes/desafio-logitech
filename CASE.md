# 📦 Desafio Técnico – LogiTech

## 📌 Cenário de Negócio
A **LogiTech** é uma empresa de logística que enfrenta desafios na **distribuição de carga dos pedidos** em seus caminhões. Atualmente, a alocação de cargas é manual, resultando em **ineficiências operacionais**, como:
- 🚛 Uso excessivo de caminhões, aumentando custos.
- ⏳ Atrasos na entrega devido à má distribuição de peso.
- ❌ Risco de sobrecarga nos veículos.

A empresa quer uma **solução automatizada** para **otimizar a distribuição de pedidos nos caminhões**.

---

## 🎯 Objetivo do Desafio
Criar um sistema que:
1. **Gerencie pedidos** (cada pedido tem um peso).
2. **Defina o peso máximo por caminhão** (configurável).
3. **Distribua os pedidos de forma eficiente**, minimizando o número de caminhões.
4. **Disponibilize uma API REST** para integração.
5. (Extra) Criar um **frontend para entrada de dados**.

---

## 📌 Regras de Negócio
1. Cada caminhão tem um **peso máximo permitido**.
2. **Nenhum pedido pode ser dividido** entre caminhões.
3. O **número de caminhões deve ser minimizado**.
4. Se um pedido for **maior que a capacidade do caminhão**, ele deve ser rejeitado.
5. O usuário pode **consultar a distribuição de pedidos** a qualquer momento.

---

## 📌 Exemplo de Entrada e Saída
### Entrada:
```json
{
    "pedidos": [
        {"id": 1, "peso": 10},
        {"id": 2, "peso": 20},
        {"id": 3, "peso": 30},
        {"id": 4, "peso": 40},
        {"id": 5, "peso": 50}
    ],
    "peso_maximo_caminhao": 60
}

### Saida:
[
    [{"id": 5, "peso": 50}],
    [{"id": 4, "peso": 40}, {"id": 1, "peso": 10}],
    [{"id": 3, "peso": 30}, {"id": 2, "peso": 20}]
]

