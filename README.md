# gabinete-do-tchola-TCG-API

Minha tentativa de fazer um card game online, e estudar arquitetura hexagonal no processo.

## Descrição

Projeto aleatório para tentar criar um card games online.

Este repositório contém a API que centralizará as partidas de um jogo online de cartas.

O frontend do jogo provavelmente será feito em um repositório a parte.

## Regras do jogo

- Cada jogador tem a chance de montar / editar seus decks antes do início do jogo
- No início da partida cada jogador saca 5 cartas
- Em sua vez, cada jogador pode baixar 1 carta na mesa
- Existem cartas de **personagens** e cartas de **items**
- Uma carta **não pode atacar** no mesmo turno em que foi **baixada**
- Após baixar a carta, inicia-se a fase de ataque (automática)
- Caso haja cartas do oponente na mesa, elas sempre serão o alvo das cartas atacantes
- Caso não haja cartas do oponente na mesa, as cartas atacantes atacam diretamente o herói do oponente
- As cartas de **itens** devem ser baixadas sempre sobre outro **personagem**, elas servem para buffar ou aplicar efeitos a eles
- Ao zerar a vida, cartas morrem
- Ao zerar a vida do herói, o player perde o jogo

## Stack

- Python
- Pytest
- Flask
- SQLAlchemy

## Dev

### Setup para desenvolvimento

- Dentro da pasta `card_game`, inicie um ambiente virtual

```sh
cd card_game
python -m venv .venv
source .venv/bin/activate
```

- Instale as dependências

```sh
pip install --upgrade pip
pip install -r requirements.txt
```

- Inicialize o banco de dados com o script `db_init.py`

```sh
python db_init.py
```

- Suba o servidor de testes com o comando

```sh
flask run --debug
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

### Testando endpoints

Testando o endpoint de hello

```sh
curl -X GET http://localhost:5000/
```

Testando o endpoint que testa o DB

```sh
curl -X GET http://localhost:5000/test_db
```

Iniciando um game via endpoint

```sh
curl -X POST http://localhost:5000/game/start \
    -H "Content-Type: application/json" \
    -d '{
            "players": [1, 2],
            "winner": null,
            "turn": true,
            "active": true
        }'
```
