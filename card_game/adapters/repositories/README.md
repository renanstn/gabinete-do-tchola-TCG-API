# Adapters

Implementações específicas para bancos de dados (PostgreSQL, SQLite).

A declaração das models em `models/` devem ser **agnósticas** de framework.

A `base` deve determinar a interface com os métodos que todos os repositories (sqlite, postgres, etc) devem conter.

O `factory` deve, com base no valor de `AppSettings.REPOSITORY` retornar uma instância de uma sessão do banco selecionado (sqlite ou postgres) pronta para uso.

Os arquivos `slite` e `postgres` herdam de base e implementam suas coisas de seus jeitos.
