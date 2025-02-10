📢 Desafio Técnico – LogiTech: Otimização de Carga de Caminhões

📝 Introdução

A LogiTech é uma empresa de logística especializada em transporte de cargas fracionadas. Seus clientes incluem grandes redes varejistas, distribuidores e e-commerces, que confiam na empresa para entregar pedidos de forma eficiente e dentro dos prazos estabelecidos.

Atualmente, a distribuição das cargas nos caminhões é feita manualmente, o que resulta em diversos problemas operacionais:

🚛 Subutilização da frota, gerando custos desnecessários.

⏳ Atrasos na expedição, pois os funcionários perdem tempo tentando organizar os pedidos nos caminhões.

❌ Sobrepeso em alguns caminhões, causando riscos de multas e acidentes.

🔄 Falta de um processo estruturado, o que dificulta escalabilidade e rastreabilidade.

Diante disso, a empresa busca uma solução automatizada para distribuir os pedidos nos caminhões de forma otimizada, garantindo que os veículos sejam preenchidos de maneira eficiente, respeitando a capacidade máxima permitida e reduzindo o número de caminhões necessários para cada entrega.

🎯 Objetivo do Desafio

Criar um sistema de gestão de carga que permita à LogiTech:
1️⃣ Cadastrar pedidos, onde cada pedido tem um peso específico.
2️⃣ Definir o peso máximo suportado por cada caminhão (essa capacidade varia de acordo com as rotas e contratos).
3️⃣ Distribuir automaticamente os pedidos entre os caminhões disponíveis, garantindo que nenhum caminhão ultrapasse seu limite de carga e que a quantidade de veículos utilizados seja otimizada.
4️⃣ Disponibilizar uma API RESTful para integração com outros sistemas da empresa.
5️⃣ (Extra) Criar um frontend para facilitar a entrada e visualização dos pedidos.

📉 Regras de Negócio

1️⃣ Cada caminhão tem um peso máximo permitido, definido pela LogiTech de acordo com regulamentações de transporte e capacidade dos veículos.
2️⃣ Nenhum pedido pode ser fracionado. Se um pedido pesa 40kg, ele deve ser alocado completamente em um único caminhão.
3️⃣ O sistema deve minimizar o número de caminhões utilizados, buscando sempre a melhor alocação de carga.
4️⃣ Pedidos que excedam a capacidade máxima de um caminhão devem ser rejeitados. Se um caminhão comporta no máximo 100kg e um pedido tem 120kg, esse pedido não pode ser transportado.
5️⃣ O usuário pode solicitar a distribuição dos pedidos a qualquer momento, verificando a melhor forma de carregamento disponível.

🔄 Fluxo Operacional

A solução proposta deve funcionar da seguinte forma:

1️⃣ Cadastro do peso máximo dos caminhões:

A LogiTech define a capacidade máxima de carga permitida por caminhão.

Esse valor pode variar por contrato ou tipo de rota (exemplo: caminhões urbanos podem ter limite de 60kg, enquanto caminhões interestaduais podem levar 100kg).

2️⃣ Cadastro dos pedidos a serem transportados:

Cada pedido possui um identificador único e um peso em quilogramas.

Os pedidos são enviados para o sistema conforme são gerados pelo time de operações.

3️⃣ Distribuição automática dos pedidos nos caminhões:

O sistema analisa os pedidos cadastrados e distribui-os entre os caminhões de forma otimizada.

Nenhum caminhão pode receber um peso superior ao permitido.

O número de caminhões usados deve ser o menor possível para reduzir custos.

4️⃣ Visualização e acompanhamento da distribuição:

A empresa pode consultar a distribuição dos pedidos e verificar como os caminhões foram preenchidos.

Caso um pedido não possa ser transportado, ele deve ser sinalizado como "não alocado" com uma justificativa.

🌟 Expectativas da Solução

1️⃣ API REST (Obrigatório)

A solução deve fornecer endpoints para:
✅ Configurar o peso máximo permitido dos caminhões.
✅ Cadastrar pedidos de forma dinâmica.
✅ Executar a distribuição de pedidos de forma otimizada.
✅ Retornar os pedidos que não puderam ser transportados.

2️⃣ Algoritmo de Distribuição (Obrigatório)

A lógica deve garantir:
✅ Respeito ao peso máximo dos caminhões.
✅ Minimização do número de caminhões necessários.
✅ Tratamento de pedidos que excedem a capacidade.

3️⃣ Testes Automatizados (Opcional)

Os candidatos podem incluir testes para:
✅ Validar se os pedidos são alocados corretamente.
✅ Garantir que pedidos muito grandes sejam rejeitados.

4️⃣ Frontend Básico (Opcional)

Se o candidato quiser se destacar, pode criar uma interface que:
✅ Permita inserir pedidos e configurar caminhões.
✅ Exiba visualmente como os caminhões estão sendo carregados.

🛠 Como Participar?

1️⃣ Faça um Fork deste repositório no GitHub.
2️⃣ Desenvolva a solução no seu próprio repositório.
3️⃣ Submeta um Pull Request com sua implementação.

🚀 Boa sorte!

