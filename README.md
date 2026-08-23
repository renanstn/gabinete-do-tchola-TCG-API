# Gabinete do Tchola TCG API

API de um jogo de cartas em desenvolvimento, usada também para estudar
arquitetura hexagonal.

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

## Arquitetura

O núcleo é dividido em três partes:

- `card_game/domain`: entidades e regras de negócio puras. Não importa Flask,
  banco de dados ou arquivos.
- `card_game/application`: casos de uso, comandos e portas (`ports`). Depende
  apenas do domínio.
- `card_game/adapters`: implementações das portas e entradas externas. Flask é
  um adaptador de entrada; JSON de deck e repositório em memória são
  adaptadores de saída.

`card_game/app.py` é o ponto de composição. É o único lugar que escolhe e
conecta os adaptadores concretos aos casos de uso.

O repositório em memória é propositalmente o padrão atual: as partidas existem
somente enquanto o processo estiver em execução. Para persistência, implemente
um novo adaptador que satisfaça `application.ports.game_repository.GameRepository`;
o domínio e os casos de uso não devem conhecer SQLAlchemy.

## Desenvolvimento

### Windows (PowerShell)

```powershell
cd card_game
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
flask --app app run --debug
```

Se o PowerShell bloquear a ativação, execute antes:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Linux / macOS (Bash)

```sh
cd card_game
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest
flask --app app run --debug
```

## Próximos adaptadores

- Repositório persistente de partidas (SQLite/PostgreSQL).
- API para jogar carta e encerrar turno.
- Catálogo e edição de decks.
- Autenticação e associação entre usuário e jogador.
