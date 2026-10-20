# Arquivo de progresso (`docs/prd_progress.json`)

Registro determinístico e legível por máquina do estado de implementação de cada RF. Esta skill cria e atualiza o arquivo com `scripts/progress.py`; skills de implementação, avaliação e correção (as que pegam um RF, implementam, avaliam e corrigem em ciclo) leem e escrevem nele durante os próprios ciclos. Nunca escreva o JSON à mão: o script deriva os campos do PRD e aplica o contrato de merge; à mão, o estado de execução se perde.

## Estrutura

```json
{
  "schema_version": 1,
  "prd_path": "docs/PRD.md",
  "generated_at": "2026-10-19T14:30:00Z",
  "features": {
    "RF-001": {
      "name": "Acesso de dono e barbeiro",
      "priority": 1,
      "wave": 1,
      "dependencies": [],
      "status": "pending",
      "cycles": 0,
      "failure_reason": null,
      "report_path": null,
      "started_at": null,
      "updated_at": "2026-10-19T14:30:00Z",
      "completed_at": null
    }
  }
}
```

`generated_at` é fixado na primeira criação e preservado nas regenerações. `prd_path` é atualizado a cada execução. Chaves de `features` são os IDs `RF-NNN`, em ordem numérica.

## Campos por RF

- `name`, `priority`, `wave`, `dependencies`: copiados da tabela e das ondas da seção 8 do PRD. Atualizados a cada regeneração.
- `status`, um de:
  - `pending`: não iniciado.
  - `implementing`: a skill de implementação está rodando. Transitório; raramente aparece em um arquivo parado.
  - `implemented`: implementação terminou e o RF aguarda veredito do avaliador no ciclo implementar → avaliar → corrigir. Persiste entre execuções.
  - `done`: avaliador aprovou; o contrato do RF foi honrado.
  - `fail`: avaliador reprovou de forma terminal, ou a implementação abortou, ou o orçamento de ciclos acabou.
  - `pr-blocked`: implementado e aprovado, mas o pull request não pôde ser aberto por conflito de merge que a correção automática não resolveu. A implementação está boa; só a integração com a branch principal está travada, e a resolução é humana.
  - `removed`: o RF existia em uma revisão anterior do PRD e não está mais na atual.
- `cycles`: quantos ciclos de correção o RF consumiu. Sempre maior ou igual a zero.
- `failure_reason`: obrigatório em `fail` e `pr-blocked`; frase curta (até 200 caracteres) com a causa. Pode persistir em `removed` como registro. `null` nos demais.
- `report_path`: caminho do último relatório de avaliação do RF, quando houver. Persiste em `removed`.
- `started_at`: quando o status saiu de `pending` pela primeira vez. Zerado só quando um RF `removed` volta ao PRD.
- `updated_at`: última escrita nesta entrada. Sempre preenchido.
- `completed_at`: quando o status virou `done`. `null` nos demais.

Todos os horários em UTC, RFC 3339 (`2026-10-19T14:30:00Z`).

## Contrato de merge (o que `progress.py` faz)

Por ID, e IDs são imutáveis:

- **RF no PRD e no arquivo, status diferente de `removed`:** preserva `status`, `cycles`, `failure_reason`, `report_path`, `started_at`, `completed_at`. Atualiza `name`, `priority`, `wave`, `dependencies` a partir do PRD, e só então mexe em `updated_at`, e só se algum desses mudou.
- **RF no PRD e no arquivo com status `removed` (voltou):** o ciclo recomeça. `pending`, `cycles` 0, campos opcionais `null`, dados do PRD atualizados, `updated_at` agora.
- **RF só no PRD (novo):** entrada nova como na primeira criação.
- **RF só no arquivo (saiu do PRD):** a entrada fica. Se ainda não era `removed`, vira `removed` com `updated_at` agora. `cycles`, `failure_reason`, `report_path`, `started_at` e `completed_at` ficam como registro. Entrada nunca é apagada, porque issues, commits e relatórios podem citá-la.

Campos que outras skills tenham acrescentado a uma entrada são preservados.

## Garantias e casos de borda

- Escrita atômica: o script grava em `.tmp` e renomeia. Outra skill nunca vê um arquivo pela metade.
- O script se recusa a gerar o progresso de um PRD que não passa no `validate.py`: progresso de PRD quebrado é pior que nenhum.
- Arquivo existente que não é JSON válido não é sobrescrito em silêncio: é renomeado para `prd_progress.json.broken-<timestamp>` e um arquivo novo é criado. Diga isso ao usuário.
- `schema_version` maior que a que esta skill conhece: o script para sem escrever nada. Estado de uma versão futura não pode ser rebaixado.
- Invariantes: todo RF da seção 6 do PRD existe em `features` (o inverso não vale, por causa dos `removed`); todo ID em `dependencies` existe em `features`; `cycles >= 0`.
