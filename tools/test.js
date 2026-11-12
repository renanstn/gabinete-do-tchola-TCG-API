'use strict';

const $ = (id) => document.getElementById(id);
let game = null;
let busy = false;
let history = [];
const json = (value) => JSON.stringify(value, null, 2);

function option(select, value, label) {
    const entry = document.createElement('option');
    entry.value = value;
    entry.textContent = label;
    select.append(entry);
}

function cardLabel(card) {
    const label = `${card.name} (${card.card_type})`;
    return card.card_type === 'character' ? `${label} | HP ${card.hp} | ATK ${card.atk}` : label;
}

function requirementDetails(card) {
    const requirements = card.play_requirements || {};
    const labels = [];
    for (const [key, reference] of Object.entries(requirements)) {
        const target = reference.name != null ? `nome "${reference.name}"` : `ID ${reference.id}`;
        if (key === 'active_stage') labels.push(`cenário ativo com ${target}`);
        if (key === 'card_on_table') labels.push(`carta na própria mesa com ${target}`);
    }
    return labels.length ? `Requer: ${labels.join(' e ')}` : 'Sem requisitos para baixar.';
}

function cardDetails(card) {
    let text = cardLabel(card);
    if (card.card_type === 'character') text += ` | pode atacar: ${card.can_attack ? 'sim' : 'não'}`;
    if (card.description) text += ` | ${card.description}`;
    if (card.card_type === 'item') {
        if (card.hp_set != null) text += ` | define HP: ${card.hp_set}`;
        if (card.atk_set != null) text += ` | define ATK: ${card.atk_set}`;
        text += ` | modifica HP: ${card.hp_modifier}, ATK: ${card.atk_modifier}, inativa: ${card.deactivate}`;
    }
    text += ` | ${requirementDetails(card)}`;
    return text;
}

function renderCards(parent, cards) {
    const list = document.createElement('ul');
    list.className = 'card-list';
    if (!cards.length) {
        const empty = document.createElement('p');
        empty.className = 'empty-zone';
        empty.textContent = 'Nenhuma carta';
        parent.append(empty);
        return;
    }
    for (const card of cards) {
        const item = document.createElement('li');
        item.className = `game-card game-card--${card.card_type}`;
        const name = document.createElement('strong');
        name.className = 'card-name';
        name.textContent = card.name;
        const category = document.createElement('span');
        category.className = 'card-category';
        category.textContent = ({ character: 'Personagem', item: 'Item', stage: 'Cenário' })[card.card_type] || card.card_type;
        const details = document.createElement('p');
        details.className = 'card-details';
        // The name and category already have their own headings.
        details.textContent = cardDetails(card).slice(`${card.name} (${card.card_type})`.length).replace(/^ \| /, '');
        item.append(category, name, details);
        if (card.items?.length) {
            const heading = document.createElement('h4');
            heading.textContent = `Itens equipados (${card.items.length})`;
            item.append(heading);
            renderCards(item, card.items);
        }
        list.append(item);
    }
    parent.append(list);
}

function renderPlayerTable(panel, player) {
    const wrapper = document.createElement('div');
    wrapper.className = 'zones-scroll';
    const table = document.createElement('table');
    table.className = 'zones-table';
    const caption = document.createElement('caption');
    caption.className = 'visually-hidden';
    caption.textContent = `Cartas de ${player.name}`;
    const head = document.createElement('thead');
    const headings = document.createElement('tr');
    const body = document.createElement('tbody');
    const row = document.createElement('tr');
    for (const [label, cards] of [
        ['Mão', player.cards_in_hand],
        ['Mesa', player.table],
        ['Cemitério', player.cemetery],
    ]) {
        const heading = document.createElement('th');
        heading.scope = 'col';
        heading.textContent = `${label} (${cards.length})`;
        headings.append(heading);
        const cell = document.createElement('td');
        renderCards(cell, cards);
        row.append(cell);
    }
    head.append(headings);
    body.append(row);
    table.append(caption, head, body);
    wrapper.append(table);
    panel.append(wrapper);
}

function updateCards() {
    const player = game.players.find((entry) => entry.id === $('move-player').value);
    $('move-card').replaceChildren();
    option($('move-card'), '', 'Selecione uma carta');
    for (const card of player.cards_in_hand) option($('move-card'), card.id, cardLabel(card));
    updateTarget();
}

function updateTarget() {
    const player = game.players.find((entry) => entry.id === $('move-player').value);
    const card = player.cards_in_hand.find((entry) => entry.id === $('move-card').value);
    const isItem = card?.card_type === 'item';
    $('move-target').disabled = !isItem;
    $('move-target').value = '';
    $('move-requirements').textContent = card ? requirementDetails(card) : 'Selecione uma carta para consultar seus requisitos.';
}

function renderGame(state) {
    game = state;
    $('game').hidden = false;
    $('game-id').value = game.game_id;
    const nameOf = (id) => game.players.find((player) => player.id === id)?.name || id;
    $('summary').textContent = `Partida: ${game.game_id} | ${game.active ? 'Em andamento' : 'Encerrada'} | Rodada: ${game.round_number ?? 'não informada'} | Cenário ativo: ${game.active_stage ? cardLabel(game.active_stage) : 'nenhum'} | Jogador ativo: ${nameOf(game.active_player_id)} | Vencedor: ${game.winner_id ? nameOf(game.winner_id) : 'nenhum'}`;
    $('state').textContent = json(game);
    $('players').replaceChildren();
    $('move-player').replaceChildren();
    $('move-target').replaceChildren();
    option($('move-target'), '', 'Sem alvo');
    for (const player of game.players) {
        option($('move-player'), player.id, `${player.name} (${player.id})`);
        const panel = document.createElement('article');
        panel.className = player.id === game.active_player_id ? 'player-panel is-active' : 'player-panel';
        const title = document.createElement('h3');
        title.textContent = `${player.name}${player.id === game.active_player_id ? ' — turno atual' : ''}`;
        const info = document.createElement('p');
        info.textContent = `ID: ${player.id} | Vida: ${player.hp} | Deck: ${player.deck_count} | Pode jogar personagem: ${player.can_play_card} | Pode jogar item: ${player.can_play_item}`;
        panel.append(title, info);
        renderPlayerTable(panel, player);
        $('players').append(panel);
        for (const card of player.table) {
            if (card.card_type === 'character') option($('move-target'), card.id, `${player.name}: ${cardLabel(card)}`);
        }
    }
    $('move-player').value = game.active_player_id;
    updateCards();
}

async function request(path, body) {
    const base = $('api-url').value.trim().replace(/\/+$/, '');
    const method = body === undefined ? 'GET' : 'POST';
    let response;
    let data;
    try {
        response = await fetch(`${base}${path}`, body === undefined ? {} : {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        const raw = await response.text();
        try { data = JSON.parse(raw); } catch { data = raw; }
    } catch (error) {
        log({ method, path, request: body, error: String(error) });
        throw new Error('Não foi possível acessar a API. Confira o endereço, a porta e se o container está rodando.');
    }
    log({ method, path, request: body, status: response.status, body: data });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${json(data)}`);
    return data;
}

function log(entry) {
    history.unshift({ time: new Date().toLocaleTimeString(), ...entry });
    history = history.slice(0, 50);
    $('response').textContent = json(history);
}

async function run(action) {
    if (busy) return;
    busy = true;
    const buttons = [...document.querySelectorAll('button')];
    buttons.forEach((button) => { button.disabled = true; });
    $('message').textContent = 'Enviando requisição...';
    try {
        const message = await action();
        $('message').textContent = message || 'Operação concluída.';
    } catch (error) {
        $('message').textContent = error.message;
    } finally {
        busy = false;
        buttons.forEach((button) => { button.disabled = false; });
    }
}

function gamePath() {
    const id = $('game-id').value.trim();
    if (!id) throw new Error('Informe o ID da partida.');
    return `/game/${encodeURIComponent(id)}`;
}

function currentGamePath() {
    const path = gamePath();
    if (!game || $('game-id').value.trim() !== game.game_id) {
        throw new Error('Carregue a partida informada antes de fazer uma jogada.');
    }
    return path;
}

$('check-api').addEventListener('click', () => run(async () => {
    await request('/');
    return 'API acessível. Veja a resposta no histórico.';
}));
$('start-game').addEventListener('click', () => run(async () => {
    const result = await request('/game/start', {
        players: [1, 2].map((index) => ({
            name: $(`player${index}-name`).value,
            deck_id: $(`player${index}-deck`).value.trim(),
        })),
    });
    $('game-id').value = result.game_id;
    renderGame(await request(gamePath()));
    return 'Partida criada e carregada.';
}));
$('load-game').addEventListener('click', () => run(async () => {
    renderGame(await request(gamePath()));
}));
$('active-player').addEventListener('click', () => run(async () => {
    const result = await request(`${gamePath()}/active-player`);
    return `Jogador ativo: ${result.active_player_id}`;
}));
$('play-card').addEventListener('click', () => run(async () => {
    const path = currentGamePath();
    const body = { player_id: $('move-player').value, card_id: $('move-card').value };
    if (!body.card_id) throw new Error('Selecione uma carta na mão.');
    if (!$('move-target').disabled && $('move-target').value) body.target_card_id = $('move-target').value;
    renderGame(await request(`${path}/play-card`, body));
}));
$('end-turn').addEventListener('click', () => run(async () => {
    renderGame(await request(`${currentGamePath()}/end-turn`, { player_id: $('move-player').value }));
}));
$('move-player').addEventListener('change', updateCards);
$('move-card').addEventListener('change', updateTarget);
$('clear-log').addEventListener('click', () => {
    history = [];
    $('response').textContent = 'Nenhuma requisição.';
});
