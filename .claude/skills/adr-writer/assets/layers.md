# Camadas da stack

Vocabulário válido para o campo `layer` do front-matter dos ADRs. `scripts/audit.py` lê a
primeira coluna desta tabela e rejeita qualquer `layer` que não esteja nela.

Uma camada entra aqui **pelo ADR que a criou**, no mesmo commit desse ADR. A tabela é
consequência de uma decisão registrada, não um arquivo que alguém edita à parte — é isso
que impede o acervo de acumular camadas que ninguém decidiu.

`stack` é reservado e sempre válido, mesmo com a tabela vazia: marca a decisão sobre a
composição da stack em si (quais camadas existem, onde ficam as fronteiras, como elas se
conectam) em vez do interior de uma camada.

| slug | camada | responsabilidade | definida em |
|---|---|---|---|
