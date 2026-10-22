---
title: <Nome do produto ou iniciativa>
type: prd
status: draft           # draft | review | approved | archived
date: AAAA-MM-DD
owners: [<PM responsável>]
related: []
---

# PRD: [nome do produto]

## 1. Resumo executivo

[2 a 3 parágrafos: o que é o produto, para quem, qual o valor central e como funciona em alto nível. Sem stack.]

## 2. Problema e oportunidade

### O problema

**[Categoria de dor 1]**
- [impacto com número aproximado: horas por semana, reais por mês, erros por lote, clientes perdidos]
- [outro sintoma da mesma dor]
- [o que já foi tentado e não resolveu]

**[Categoria de dor 2]**
- [impacto]
- [impacto]

### A oportunidade

- **[Categoria de dor 1].** [Como o produto resolve e o que o diferencia do que existe hoje.]
- **[Categoria de dor 2].** [Como resolve.]

## 3. Público-alvo

### Usuários primários

**[Nome do perfil 1]**
- [característica ou necessidade]
- [característica ou necessidade]
- [característica ou necessidade]

**[Nome do perfil 2]**
- [característica]
- [característica]
- [característica]

### Perfil comportamental

- [característica comum a todos os perfis. Omita esta subseção quando houver um perfil só.]

## 4. Objetivos e métricas

### Objetivos de produto

| Objetivo | Métrica | Meta |
| --- | --- | --- |
| **[Verbo de ação]** [objetivo 1] | [como se mede] | [número e prazo] |
| **[Verbo]** [objetivo 2] | [métrica 2] | [meta 2] |

### Requisitos não funcionais

Performance
- [meta observável pelo usuário. ex: busca responde em até 1 segundo para 95 por cento das consultas]

Disponibilidade
- [ex: 99.9 por cento de disponibilidade mensal no horário comercial]

Segurança e autorização
- [ex: quem pode fazer o quê, por papel; alterações sensíveis registradas com autor e horário]

Compatibilidade
- [ex: navegadores dos últimos 2 anos em desktop e celular; português do Brasil]

Compliance
- [ex: dados pessoais tratados conforme a LGPD, com exclusão sob pedido em até 15 dias]

Acessibilidade
- [ex: fluxos principais operáveis por teclado e leitor de tela]

## 5. Histórias de usuário

### RF-001 [nome do requisito]
- Como [papel], quero [ação concreta] para [resultado]
- Como [papel], quero [ação] para [resultado]

### RF-002 [nome do requisito 2]
- Como [papel], quero [ação] para [resultado]
- Como o sistema, quero [ação automática] para [resultado]

## 6. Requisitos funcionais

### RF-001 [nome do requisito]
[Uma frase: o que o sistema faz neste requisito.]

**Fornece:**
- [dado ou saída que outro requisito usa, com os campos principais] (usado por RF-002)

**Capacidades:**
- [limite, formato ou regra de negócio com número: tamanho máximo, quantidade, prazo] (hipótese)
- [regra de negócio]

**Experiência:**
- [fluxo do usuário passo a passo: campos, validações, ordem, feedback visual, estados, mensagens]
- [estado vazio, carregando, sucesso]

**Tratamento de erros:**
- [cenário de falha]: [o que o usuário vê e o que acontece com o dado]
- [cenário 2]: [mensagem]

### RF-002 [nome do requisito 2]
[descrição em uma frase]

**Consome:**
- RF-001: [dado que este requisito precisa, com os campos principais]

**Fornece:**
- [dado] (usado por RF-003, RF-004)

**Escopo mínimo:**
- [capacidade sem a qual o requisito não cumpre seu propósito]

**Adições de escopo completo:**
- [capacidade que melhora o requisito depois do mínimo pronto]

**Capacidades:**
- [limite, formato ou regra com número]

**Experiência:**
- [fluxo detalhado]

## 7. Fora de escopo

**[Categoria 1]**
- [o que não entra nesta versão, e em uma palavra por quê, quando ajudar]

**[Categoria 2]**
- [item]

## 8. Dependências entre requisitos

Uma linha "B depende de A" significa: B não funciona sem A implementado antes. A coluna "Depende de" é um superconjunto dos blocos Consome. A ordem de construção (ondas, caminho crítico e diagrama) é derivada desta tabela e vive no roadmap, em "Ordem de execução".

| # | Requisito | Prioridade | Depende de |
| --- | --- | --- | --- |
| RF-001 | [nome] | 1 | nenhum |
| RF-002 | [nome] | 1 | RF-001 |
| RF-003 | [nome] | 2 | RF-002 |

### Requisitos de fundação

Estes requisitos montam a infraestrutura compartilhada do projeto. Em um projeto novo, eles são implementados em sequência, antes ou junto de qualquer requisito que dependa deles. [Omita esta subseção quando nenhum requisito tiver esse papel.]

- **RF-001 [nome]**: [o que ele monta de base para os demais]

### Níveis de prioridade

- **1** = Essencial: o produto não funciona sem isso
- **2** = Importante: agrega valor significativo
- **3** = Desejável: melhoria incremental

### Dependências externas

- **[título da dependência]**: [quem entrega o quê, descrito pelo que faz, e o que trava enquanto não chega] (trava RF-002)

## 9. Critérios de aceitação

### RF-001 [nome do requisito]
- [ ] [critério verificável de sucesso]
- [ ] [critério verificável de falha: o que acontece quando dá errado]

### RF-002 [nome do requisito 2]
- [ ] [critério]
- [ ] [critério]

### Integração entre requisitos
- [ ] [dado] produzido por RF-001 chega a RF-002 e [efeito observável]
