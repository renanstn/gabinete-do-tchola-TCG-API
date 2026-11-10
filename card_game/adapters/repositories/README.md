# Repositórios

Este diretório contém adaptadores de saída para a porta
`application.ports.game_repository.GameRepository`.

`InMemoryGameRepository` é usado no desenvolvimento e testes.
`PostgresGameRepository` usa psycopg e persiste o agregado completo em JSONB.
O mapeamento em `game_snapshot.py` preserva o estado interno do domínio,
independentemente dos schemas HTTP, e restaura objetos sem executar ações do jogo.

A escolha do adaptador acontece somente em `app.py`, por `DATABASE_URL`.
Inicialize a tabela com `flask --app app init-db`. O domínio e a aplicação
continuam dependendo exclusivamente da porta `GameRepository`.

Cada operação abre e fecha sua conexão; gravações fazem commit ou rollback ao
sair do contexto. Não há conexão global compartilhada entre requisições.
O upsert é atômico, mas a porta não protege o ciclo leitura/alteração/gravação
contra comandos concorrentes na mesma partida.
