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

O ponto de composição escolhe `PostgresGameRepository` quando `DATABASE_URL`
está definida. Sem ela, usa `InMemoryGameRepository`, útil para testes e
desenvolvimento. Ambos implementam a mesma porta; domínio e aplicação não
importam o driver PostgreSQL nem conhecem SQL ou detalhes de persistência.

## PostgreSQL

Crie um banco PostgreSQL e instale as dependências de `card_game/requirements.txt`.
Com o ambiente virtual ativo, execute dentro de `card_game`:

```powershell
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/card_game"
flask --app app init-db
flask --app app run --debug
```

Em Bash, defina a variável com
`export DATABASE_URL='postgresql://postgres:postgres@localhost:5432/card_game'`.
As credenciais acima são apenas um exemplo local. A aplicação não carrega `.env`
automaticamente; configure a variável no ambiente do processo.

`init-db` cria a tabela `games` de forma idempotente em um banco já existente.
É uma etapa explícita de instalação: iniciar a API não cria tabelas nem conecta
ao banco. Execute o comando com um usuário que possa criar tabelas; o usuário
da API precisa de permissões de leitura, inserção e atualização nessa tabela.

O adaptador salva cada partida inteira em uma coluna JSONB, com chave UUID e
versão do formato do snapshot. Isso mantém jogadores, ordem das cartas nas
quatro zonas, atributos de combate, itens equipados, turno e vencedor juntos.
Cada `save` insere ou atualiza a partida em uma transação; leituras retornam
novas entidades do domínio. Falhas do banco são propagadas, sem fallback para
memória. O schema inicial está em
`card_game/adapters/repositories/postgres_schema.sql`; mudanças futuras no schema
ou no formato dos snapshots precisam de migrações próprias.

A porta atual separa leitura e gravação e não oferece controle de concorrência.
Comandos simultâneos sobre a mesma partida podem sobrescrever alterações:
a última gravação prevalece. O snapshot atômico não serializa o caso de uso inteiro.

Os testes de integração usam um banco separado, informado em `TEST_DATABASE_URL`:

```powershell
$env:TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/card_game_test"
python -m pytest
```

Sem essa variável, somente os testes de integração PostgreSQL são ignorados.
Eles criam a tabela quando necessário e removem as partidas que geram. O workflow
`validate-db.yml` executa esses testes com um serviço PostgreSQL 16.

## Desenvolvimento com Docker (recomendado)

Instale o Docker com Compose v2 (no Windows/macOS, Docker Desktop com containers
Linux). Execute os comandos abaixo na raiz do repositório; não é necessário
instalar Python ou PostgreSQL na máquina.

```sh
docker compose up --build -d
docker compose logs -f api
```

A API fica em http://localhost:5000. Para conferir:

```sh
curl http://localhost:5000/
```

O retorno esperado é `{"service":"card-game"}`. O Compose espera o healthcheck
do PostgreSQL e executa `flask --app app init-db` antes de iniciar a API.
O código em `card_game` é montado no container e o Flask roda com `--debug`,
recarregando alterações nos arquivos Python. Ao mudar `requirements.txt`, execute
`docker compose up --build -d` novamente. Esta configuração usa o servidor de
desenvolvimento e credenciais locais; destina-se ao ambiente de dev.

O banco de desenvolvimento fica disponível em `localhost:5432`, com banco
`card_game`, usuário `postgres` e senha `postgres`. Dentro da rede dos containers,
a API usa o hostname `db`. Os dados ficam no volume nomeado `postgres_data`,
preservado entre reinicializações. As portas publicadas ficam restritas à máquina
local. Para trocar as portas, crie um `.env` na raiz (lido pelo Compose):

```dotenv
API_PORT=5001
POSTGRES_PORT=5433
```

Nesse exemplo, acesse a API em http://localhost:5001. As portas internas e a URL
usada pela API continuam as mesmas.

### Testes nos containers

Para executar a suíte completa, incluindo os testes de integração PostgreSQL:

```sh
docker compose --profile test run --build --rm tests
```

Esse comando inicia um PostgreSQL separado (`test-db`) e fornece
`TEST_DATABASE_URL` ao pytest. O banco de testes não publica portas e usa
armazenamento temporário, sem acessar os dados do desenvolvimento. É possível
executá-lo sem subir a API. Para selecionar apenas os testes do repositório:

```sh
docker compose --profile test run --build --rm tests python -m pytest tests/adapters/test_postgres_game_repository.py -v
```

### Comandos úteis

```sh
docker compose ps
docker compose logs -f db
docker compose exec db psql -U postgres -d card_game
docker compose --profile test down
```

`down` encerra e remove os containers, mantendo os dados do desenvolvimento.
Para apagar também o volume e começar com um banco vazio, execute
`docker compose --profile test down -v` (**apaga todas as partidas locais**).

## Desenvolvimento sem Docker

### Windows (PowerShell)

```powershell
cd card_game
py -3.12 -m venv .venv
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

- API para jogar carta e encerrar turno.
- Catálogo e edição de decks.
- Autenticação e associação entre usuário e jogador.
