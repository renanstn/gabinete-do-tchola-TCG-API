# Domain

Toda a lógica do jogo fica aqui, escrita em Python puro.

## Cartas

`card.py` define `Card`, uma base abstrata com identidade e apresentação
(`id`, `name`, `description`, `image`, `sound`), e três subclasses:

- `CharacterCard(hp, atk, name, ...)`: estado de combate, dano, ativação e
  aplicação de itens. Apenas personagens possuem `items`.
- `ItemCard(name, ...)`: efeitos relativos, absolutos e de inativação,
  com validação antes da aplicação.
- `StageCard(name, ...)`: identidade de cenário. As regras para jogar cenários
  ainda não estão implementadas; essas jogadas continuam sendo rejeitadas.

`card_type` é uma propriedade somente de leitura, definida pela subclasse.
Deck, mão e cemitério aceitam `Card`; a mesa é uma lista de `CharacterCard`.

```python
hero = CharacterCard(hp=5, atk=3, name="Herói")
sword = ItemCard(name="Espada", atk_modifier=2)
hero.apply_item(sword)
```

O JSON dos decks continua usando `card_type` para escolher a classe concreta.
Personagens exigem `hp` e `atk`; campos antigos de combate em itens e cenários
são ignorados na leitura. A resposta HTTP inclui somente os campos pertinentes
à categoria: clientes devem consultar `card_type` antes de acessar esses campos.

Snapshots novos usam versão 2, com campos específicos de cada categoria.
Snapshots da versão 1 continuam sendo lidos. A restauração preserva os tipos e
o estado de combate salvo, sem reaplicar efeitos de itens.
