# Template agnóstico por contrato de alvos e CI sem stack

## Contexto e problema

O roteiro previa "stack e CI" como passo 3, mas o objetivo do template é servir a qualquer
linguagem. Como entregar CI útil e uma interface estável para agentes sem escolher uma stack?

## Opções consideradas

* Base agnóstica com contrato de alvos no `Makefile` e CI só com verificações universais
* Um template por stack, derivado da base (sem herança no GitHub; cópias mantidas à mão)
* Perfis de stack dentro do template, com `scripts/init.sh --stack` (modelo cookiecutter e copier)
* Nunca ter stack: só padrões e harness; cada projeto refaz a CI

Verificações universais consideradas: actionlint, gitleaks, editorconfig-checker, markdownlint.
Fixação das actions: SHA completo com comentário de versão, ou tag major.

## Decisão

Opção escolhida: "base agnóstica com contrato de alvos", porque mantém um único template, dá aos
agentes uma interface fixa (`make lint`, `format`, `test`, `build`) que não muda quando a stack
entra, e a CI roda o mesmo `make check` usado localmente. Perfis de stack ficam como possível
passo futuro, se houver demanda real.

Detalhes:

* Alvos do contrato sem `scripts/<alvo>.sh` avisam e passam, sem bloquear. Assim o template e o projeto recém-gerado têm CI verde.
* Verificações universais adotadas agora: actionlint (valida os workflows) e gitleaks (segredos).
  editorconfig-checker e markdownlint ficam como candidatos.
* `pr-title` valida o título do PR com `amannn/action-semantic-pull-request`, mesmas regras do
  hook, porque com squash é o título que vira o commit em `main`.
* Actions fixadas por SHA completo com comentário da versão (recomendação do GitHub e do OpenSSF).
  Sem Dependabot por enquanto: a atualização dos SHAs é manual.
* `check`, `secrets` e `pr-title` são status checks obrigatórios no ruleset de `main`.
  (Revisão de 2026-10-17: o job `secrets` foi absorvido por `check-secrets`, que passou a varrer o
  histórico; restam `check` e `pr-title`.)

### Consequências

* Bom, porque o template continua servindo a qualquer linguagem e `AGENTS.md` não muda com a stack.
* Bom, porque local e CI rodam o mesmo comando; o que passa aqui passa lá.
* Ruim, porque `make lint` e `make test` passam sem fazer nada até a stack ser implementada; o
  aviso é visível, mas não bloqueia.
* Ruim, porque os SHAs das actions envelhecem sem Dependabot; revisar a cada release.
