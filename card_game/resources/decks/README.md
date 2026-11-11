Nessa pasta ficarÃ£o registrados em JSON os diversos decks disponÃ­veis no jogo.

Na subpasta `images/{deck_name}/` devem ser colocadas as imagens das cartas de cada deck

### Cartas de item

Use `"card_type": "item"` e os campos opcionais `hp_modifier` e
`atk_modifier` (inteiros positivos para aumentar ou negativos para reduzir)
e `deactivate` (booleano). Os modificadores padrÃ£o sÃ£o zero e `deactivate`
Ã© `false`. Um item pode combinar efeitos. `hp` e `atk` do prÃ³prio item
podem ser omitidos; eles nÃ£o sÃ£o os modificadores do alvo.

Para substituir um atributo, use `hp_set` (vida atual) ou `atk_set`
(ataque). Omitir esses campos ou usar `null` mantÃ©m o valor atual;
zero Ã© um valor vÃ¡lido. Exemplos de definiÃ§Ãµes completas:

```json
[
  {"name": "Vitalidade", "card_type": "item", "hp_modifier": 3},
  {"name": "Fragilidade", "card_type": "item", "hp_set": 1},
  {"name": "ForÃ§a", "card_type": "item", "atk_modifier": 2},
  {"name": "Poder Fixo", "card_type": "item", "atk_set": 5}
]
```

Um item nÃ£o pode misturar os modos de substituiÃ§Ã£o e modificaÃ§Ã£o relativa.
Se qualquer `*_set` estiver definido (inclusive zero), ambos os
`*_modifier` devem ser zero, seu valor padrÃ£o. Isso tambÃ©m proÃ­be misturas
entre atributos, como `hp_set: 1` com `atk_modifier: 2`.
Ã‰ permitido combinar `hp_set` com `atk_set`, ou `hp_modifier` com
`atk_modifier`. `deactivate` pode acompanhar qualquer modo.
DefiniÃ§Ãµes incompatÃ­veis sÃ£o rejeitadas com `ValueError` ao criar ou
carregar a carta, e a regra Ã© revalidada antes de aplicar o item.
O ataque final tem mÃ­nimo zero; vida final menor ou igual a zero mata
o personagem.

`hp_set` altera somente a vida atual, preservando `initial_hp`. JÃ¡
`hp_modifier` continua alterando ambas. As substituiÃ§Ãµes sÃ£o imediatas:
um item posterior pode modificar o valor normalmente, sem que o valor
fixado pelo item anterior seja reaplicado.

```json
{
  "name": "Rede AmaldiÃ§oada",
  "card_type": "item",
  "hp_modifier": -1,
  "atk_modifier": -2,
  "deactivate": true
}
```

Os efeitos sÃ£o imediatos e acumulÃ¡veis. A vida atual e a vida inicial do
personagem recebem o modificador de vida, preservando o dano jÃ¡ sofrido.
Vida menor ou igual a zero envia o personagem ao cemitÃ©rio. O ataque tem
mÃ­nimo zero. A inativaÃ§Ã£o impede a prÃ³xima fase de ataque do dono do
personagem; ele Ã© reativado ao final dessa fase. Reaplicar a inativaÃ§Ã£o antes
dessa fase nÃ£o acumula turnos de bloqueio.

Itens ficam vinculados ao personagem em `items`, inclusive no cemitÃ©rio,
e nÃ£o ocupam espaÃ§os da mesa. Jogar um item consome a Ãºnica jogada de carta
do turno, mesmo quando o alvo pertence ao oponente.
