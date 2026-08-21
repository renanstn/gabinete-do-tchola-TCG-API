# Repositórios

Este diretório contém adaptadores de saída para a porta
`application.ports.game_repository.GameRepository`.

`InMemoryGameRepository` é usado no desenvolvimento e testes. Um adaptador
SQLite ou PostgreSQL deverá mapear seu modelo de persistência para as entidades
do domínio, sem ser importado pela camada `application`.
