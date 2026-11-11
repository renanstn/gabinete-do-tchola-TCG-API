# Tools

Com Docker Compose, execute na raiz do repositório:

```sh
docker compose up --build -d
```

A ferramenta é servida pelo Nginx em http://localhost:8080/test.html. Para mudar a porta,
defina `TOOLS_PORT=8081` no `.env` da raiz.

A ferramenta chama a API em `http://127.0.0.1:5000`; se alterar `API_PORT`,
ajuste o campo **Endereço da API** na página. Os dois jogadores já vêm
preenchidos com o deck disponível no projeto:
`6c2e32a4-644d-4be5-bd8a-62b683b08757`.

## Testando uma partida

1. Clique em **Iniciar partida** para criar e carregar o estado completo.
2. Confira a vida, a quantidade de cartas no deck, as mãos, mesas e cemitérios.
3. Selecione uma carta na mão do jogador ativo e clique em **Jogar carta**.
   Para itens, selecione também um personagem na mesa de qualquer jogador.
4. Clique em **Encerrar turno** para executar os ataques automáticos e passar
   a vez. O estado e o jogador selecionado são atualizados após cada ação.
5. Para retomar uma partida, informe seu UUID e clique em
   **Carregar / atualizar estado**. O botão **Consultar jogador ativo**
   consulta esse endpoint separadamente.

O vencedor aparece quando a partida termina. As cartas mostram atributos,
possibilidade de atacar, modificadores e itens equipados. O estado completo
também está disponível em JSON.

É possível selecionar o outro jogador para testar a rejeição de jogadas fora
do turno. A API valida as regras; erros HTTP e os corpos das requisições e
respostas aparecem no histórico das últimas 50 requisições. Se outro cliente
alterar a partida, use **Carregar / atualizar estado** para sincronizar.

Esta ferramenta exibe as mãos dos dois jogadores e se destina a testes locais.

## Sem Docker

Para testar o jogo com este html, suba um servidorzinho com o comando

```
cd tools
python -m http.server 8080
```

E acesse:

http://localhost:8080/test.html
