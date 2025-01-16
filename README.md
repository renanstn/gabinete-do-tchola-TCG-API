# gabinete-do-tchola-TCG-API

Um card games sobre memes internos...

## Descrição

Projeto aleatório para tentar criar um card games online.

Este repositório contém a API que centralizará as partidas de um jogo online de cartas.

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
