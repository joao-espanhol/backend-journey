# Dias 9-10 — Fase 1 (Python Sólido) — Capstone: projeto `brewlog`

> Dias 9 e 10 foram fundidos em uma única frente de trabalho: a construção do
> mini-projeto capstone da Fase 1. Não houve bloco de exercícios isolados — **o
> projeto é o exercício**.
>
> **O projeto `brewlog` não vive neste repositório.** Por ter atingido qualidade
> de projeto autônomo (pacote estruturado em camadas, 90 testes), foi destacado
> para um repositório próprio:
>
> **→ https://github.com/joao-espanhol/brewlog**
>
> Estas notas registram o contexto pedagógico dos dias 9-10 e as decisões de
> arquitetura tomadas durante a construção. A documentação de uso, instalação e
> execução do projeto está no README do repositório acima.

---

## 1. O que foi construído

CLI de gerenciamento de uma cervejaria artesanal (contexto do projeto pessoal
Rato de Convés), em Python puro, sem dependências externas além de pytest para
os testes. Gerencia quatro domínios:

- **Catálogo de ingredientes**: `Malt`, `Hop`, `Yeast` (dataclasses frozen).
- **Receitas** (`Recipe`): combinam ingredientes do catálogo com quantidades,
  além de OG/FG/IBU alvo.
- **Lotes** (`Batch`): uma brassagem real de uma receita, com valores medidos
  (OG/FG/volume reais) e métricas derivadas (ABV real, desvios, atenuação).
- **Persistência** (`store`): serialização para JSON e reconstrução dos objetos.

O objetivo pedagógico dos dias 9-10 era **integrar tudo o que foi visto na Fase
1** — mutabilidade, OOP, dataclasses, herança/ABC, exceções customizadas,
type hints, módulos/pacotes e pytest — em um único projeto coeso, com cara de
código real e não de exercício.

---

## 2. Conceitos da Fase 1 exercitados no capstone

| Conceito (dia de origem)              | Onde aparece no brewlog                              |
|---------------------------------------|-----------------------------------------------------|
| Mutabilidade (Dias 1-2)               | frozen no catálogo; estado passado por parâmetro    |
| OOP, `@property`, dunder (Dias 3-4)   | entidades de domínio, `__post_init__`, `__eq__`     |
| ABC + `@abstractmethod` (Dias 3-4)    | `Ingredient` base de `Malt`/`Hop`/`Yeast`           |
| Exceções customizadas (Dias 7-8)      | hierarquia `BrewlogError` e derivadas               |
| Type hints (Dias 7-8)                 | assinaturas de todos os métodos e funções           |
| Módulos e pacotes (Dias 9-10)         | estrutura `domain/` + `services/` + imports absolutos|
| pytest (Dias 9-10)                    | 90 testes com fixtures, `match=`, `monkeypatch`     |

---

## 3. Decisões de arquitetura (registro pedagógico)

As decisões abaixo foram deliberadas e travadas durante a construção. Estão aqui
porque **são o aprendizado dos dias 9-10** — não repetem o README do projeto, que
foca em uso.

### 3.1 Ordem de validação: valor antes de relacional

Validação de valor (`BrewlogInvalidValueError`) vem **antes** de validação
relacional (`BrewlogNotFoundError` / `BrewlogConflictError`). Um método que
recebe nome vazio e um catálogo valida o nome primeiro; só depois checa o
catálogo. Ordem invertida produz mensagens de erro enganosas ("não encontrado"
quando o problema real é "nome vazio").

### 3.2 Estado passado por parâmetro, nunca por escopo de módulo

As cinco coleções (`malts, hops, yeasts, recipes, batches`) são passadas como
argumentos entre todas as funções que podem alcançar um `save()`. Mesmo funções
que usam só parte delas recebem as cinco. Estado global tornaria o fluxo de
dados implícito e os testes dependeriam de monkeypatch em estado global; por
parâmetro, cada função declara suas dependências e os testes injetam coleções
controladas.

### 3.3 `save()` após cada operação que modifica dados

Não se salva uma vez no fim do programa: cada create/delete chama `save()`
imediatamente. Se o programa crashar numa sessão longa, save-no-fim perderia
tudo; save incremental limita a perda ao que estava sendo digitado.

### 3.4 `FileNotFoundError` tratado só em `main()`

`load()` deixa `FileNotFoundError` propagar. O único ponto que trata é `main()`,
na primeira execução: arquivo não existe → cria vazio → recarrega. Em todo o
resto do app, a exceção propaga naturalmente.

### 3.5 Geração de `batch_id` na CLI, antes de instanciar

`batch_id` (`"BATCH_001"`, `"BATCH_002"`...) é calculado contando os batches
existentes e formatado com zero-padding (`:03d`), **antes** de instanciar
`Batch(...)`. O id faz parte da identidade do batch desde o nascimento — nunca
criar o objeto sem id e completar depois. O id não é reutilizado após deleção
(parte do maior id existente, não do tamanho da lista), mas reinicia se a lista
é totalmente esvaziada.

### 3.6 `set_yeast(None)` é operação válida

`None` significa "remover levedura" e retorna cedo, antes da validação de string.
Um `None` não deve ser validado como se fosse um nome.

### 3.7 Retry re-pede todos os campos

O loop de criação re-pede **todos** os campos quando qualquer um falha, em vez de
descobrir qual campo errou. Descobrir o campo exigiria acoplar a CLI ao texto da
exceção; re-pedir tudo é mais simples e não acopla. Refinamento por-campo é
roadmap.

---

## 4. Pontos de correção recorrentes (dias 9-10)

Registrados para reforço nas próximas fases:

- **`return` vs `continue`/`break` em loops de menu:** cancelamentos usavam
  `return`, que saía da função de menu inteira em vez de só abortar a operação.
  Correção: `continue` (volta ao topo do `while`) ou `break` + checagem +
  `continue` nos casos aninhados. Erro recorreu em `recipes_menu` e
  `batches_menu`.
- **Direção de operador em fronteiras** (`<` vs `<=`): faixas de validação
  (`>= 0` para EBC, `0 < x < 100` exclusivo para alpha_acid e attenuation).
- **`strptime` exige `try/except`**, não checagem por truthiness: `"32/13/2025"`
  é string não-vazia e passaria por `if not date`.

---

## 5. Testes (90 no total, incluindo Dia 08)

Distribuídos em `test_recipe.py`, `test_batch.py`, `test_store.py` e
`test_cli.py`. Disciplina consolidada:

- `pytest.raises` com `match=` sempre que o método tem mais de um caminho de
  `raise` do mesmo tipo.
- Testes chamam o método real, nunca manipulam atributos direto.
- Fixtures evitam acoplamento entre testes.
- Testes de CLI usam `monkeypatch` em `builtins.input` para simular digitação e
  `capsys` para verificar a saída.

Detalhamento completo da suíte: ver README do repositório do projeto.

---

## 6. Roadmap documentado (fora de escopo do capstone)

- **Update** de receitas e itens de catálogo.
- **IBU calculado** a partir do lúpulo (hoje é entrada manual).
- **Refatoração dos três `_menu` de ingrediente** (malt/hop/yeast) para função
  genérica parametrizada — só depois dos três completos, sem abstração prematura.