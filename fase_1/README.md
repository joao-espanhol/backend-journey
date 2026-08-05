# Fase 1 — Python Sólido

Primeira fase da trilha **backend-journey**. Objetivo: eliminar as fragilidades
de fundamento em Python que comprometem entrevistas — mutabilidade, OOP,
decorators, generators, context managers, exceções, comprehensions, type hints,
módulos/pacotes e introdução a testes com pytest.

Duração: 10 dias. Ao final, um projeto capstone integra todos os conceitos.

---

## Conteúdo por dia

| Dias  | Tema                                              | Pasta                     |
|-------|---------------------------------------------------|---------------------------|
| 1-2   | Tipos mutáveis vs imutáveis; strings, f-strings   | `day_01/`, `day_02/`      |
| 3-4   | OOP: herança, encapsulamento, polimorfismo, dunder| `day_03/`, `day_04/`      |
| 5-6   | Decorators, generators, context managers          | `day_05/`, `day_06/`      |
| 7-8   | Exceptions, comprehensions, type hints, mypy      | `day_07/`, `day_08/`      |
| 9-10  | Módulos e pacotes, pytest, **projeto capstone**   | `day_09_10/` (notas)      |

Cada pasta de dia contém os exercícios daquele dia e um arquivo de notas em
Markdown com a teoria e os pontos de reforço.

---

## Capstone dos Dias 9-10 — projeto `brewlog`

Os dias 9 e 10 foram fundidos em uma única frente de trabalho: a construção de um
projeto que integra tudo o que foi visto na fase. Não houve exercícios isolados —
**o projeto é o exercício**.

O `brewlog` é uma CLI de gerenciamento de cervejaria artesanal em Python puro
(catálogo de ingredientes, receitas, lotes de produção e persistência em JSON),
com uma suíte de 90 testes em pytest.

Por ter atingido qualidade de projeto autônomo, o `brewlog` foi destacado para um
repositório próprio, fora do `backend-journey`:

### → https://github.com/joao-espanhol/brewlog

As **notas pedagógicas** dos dias 9-10 (decisões de arquitetura, conceitos
exercitados, pontos de correção recorrentes) permanecem aqui, em
[`day_09_10/notas_dia_09_10.md`](day_09_10/notas_dia_09_10.md). A **documentação
de uso** (instalação, execução, estrutura) está no README do repositório do
projeto.

---

## Conceitos consolidados na fase

- Mutabilidade e o bug do argumento padrão mutável
- OOP completo: `@property`, `__init__`/`__post_init__`, `__eq__`, `__repr__`
- Classes base abstratas (`abc.ABC`, `@abstractmethod`)
- Dataclasses, incluindo `frozen=True` e a relação com hashabilidade
- Decorators (`@wraps`, factory vs product), generators, context managers
- Hierarquias de exceções customizadas e encadeamento (`raise ... from`)
- Type hints (PEP 484) e verificação com mypy
- Módulos, pacotes e imports absolutos a partir da raiz do pacote
- pytest: fixtures, `pytest.raises(match=...)`, `monkeypatch`, `capsys`

---

## Entregável da fase

CLI `brewlog` + suíte de testes pytest, em repositório próprio. **Concluído.**