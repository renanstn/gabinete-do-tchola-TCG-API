# gabinete-do-tchola-TCG-API

Um card games sobre memes internos...

## Descrição

Projeto aleatório para tentar criar um card games online.

Este repositório contém a API que centralizará as partidas de um jogo online de cartas.

## Regras do jogo

- Cada jogador tem a chance de montar / editar seus decks antes do início do jogo
- No início da partida cada jogador saca 5 cartas
- Em sua vez, cada jogador pode baixar 1 carta na mesa
- Existem cartas de **personagens** e cartas de **items**
- Uma carta não pode atacar no mesmo turno em que foi baixada
- Após baixar a carta, inicia-se a fase de ataque
- Caso haja cartas do oponente na mesa, elas sempre serão o alvo das cartas atacantes
- Caso não haja cartas do oponente na mesa, as cartas atacantes atacam diretamente o herói do oponente
- As cartas de **itens** devem ser baixadas sempre sobre outro **personagem**, elas servem para upar ou aplicar efeitos
- Ao zerar a vida, cartas morrem
- Ao zerar a vida do herói, o player perde o jogo

## Stack

- Python
- Pytest
- Flask
- SQLAlchemy

## Dev

### Setup para desenvolvimento

- Dentro da pasta `api`, inicie um ambiente virtual

```sh
cd api
python -m venv .venv
source .venv/bin/activate
```

- Instale as dependências

```sh
pip install -r requirements.txt
```

### Comandos úteis

Executa o `black` e o `isort` para auto formatação do código:

```sh
make clean
```

Executar os testes unitários:

```sh
pytest
```
