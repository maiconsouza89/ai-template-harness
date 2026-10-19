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
| `workflow` | Fluxo de trabalho | Git, branches, commits, versionamento, licença e idioma: como o repositório recebe mudanças | 0006 |
| `harness` | Harness para agentes | CLAUDE.md, Makefile, docs/ e ADRs: o que o agente lê e executa | 0006 |
| `ci` | Integração contínua | Verificações locais e no GitHub Actions, contrato de alvos, proteção de main | 0006 |
| `release` | Release | Versão, changelog, tag e GitHub Release | 0006 |
