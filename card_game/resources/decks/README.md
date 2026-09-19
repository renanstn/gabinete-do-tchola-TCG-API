Nessa pasta ficarão registrados em JSON os diversos decks disponíveis no jogo.

Na subpasta `images/{deck_name}/` devem ser colocadas as imagens das cartas de cada deck

### Cartas de item

Use `"card_type": "item"` e os campos opcionais `hp_modifier` e
`atk_modifier` (inteiros positivos para aumentar ou negativos para reduzir)
e `deactivate` (booleano). Os modificadores padrão são zero e `deactivate`
é `false`. Um item pode combinar efeitos. `hp` e `atk` do próprio item
podem ser omitidos; eles não são os modificadores do alvo.

```json
{
  "name": "Rede Amaldiçoada",
  "card_type": "item",
  "hp_modifier": -1,
  "atk_modifier": -2,
  "deactivate": true
}
```

Os efeitos são imediatos e acumuláveis. A vida atual e a vida inicial do
personagem recebem o modificador de vida, preservando o dano já sofrido.
Vida menor ou igual a zero envia o personagem ao cemitério. O ataque tem
mínimo zero. A inativação impede a próxima fase de ataque do dono do
personagem; ele é reativado ao final dessa fase. Reaplicar a inativação antes
dessa fase não acumula turnos de bloqueio.

Itens ficam vinculados ao personagem em `items`, inclusive no cemitério,
e não ocupam espaços da mesa. Jogar um item consome a única jogada de carta
do turno, mesmo quando o alvo pertence ao oponente.
