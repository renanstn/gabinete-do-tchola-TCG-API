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

Snapshots novos usam versão 3, com campos específicos de cada categoria.
Snapshots das versões 1 e 2 continuam sendo lidos. A restauração preserva os tipos e
o estado de combate salvo, sem reaplicar efeitos de itens.


## Rodadas e requisitos para baixar cartas

Cada turno corresponde a uma rodada: `Game.round_number` começa em 1 e aumenta
uma vez por troca de jogador. Encerrar uma partida não inicia outra rodada.
O contador é persistido e exposto pela API. Snapshots antigos começam em 1,
pois não é possível recuperar seu histórico de turnos.

Todas as categorias aceitam `play_requirements`, opcional, no construtor e no
JSON dos decks:

```json
{
  "play_requirements": {
    "active_stage": {"name": "Floresta"},
    "card_on_table": {"name": "Guardião"}
  }
}
```

Cada referência deve conter exatamente `name` ou `id`, com uma string não
vazia. A comparação é literal e diferencia maiúsculas de minúsculas. Quando
presentes, ambos os requisitos devem ser atendidos antes de qualquer alteração
da jogada. `card_on_table` busca apenas personagens na mesa do próprio jogador;
cartas na mão, no cemitério ou na mesa adversária não atendem ao requisito.

O `id` atual identifica uma instância de carta e é gerado ao carregar um deck;
use `name` para referências estáveis entre definições de decks.

`Game.active_stage` é um estado opcional preparado para validar requisitos.
Ainda não existe ação para ativar ou substituir cenários, nem efeitos ou prazo
de troca. Sem cenário ativo, um requisito `active_stage` impede a jogada.
