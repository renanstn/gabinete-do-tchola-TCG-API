from flask.testing import FlaskClient


EXAMPLE_DECK_ID = "6c2e32a4-644d-4be5-bd8a-62b683b08757"


def test_start_game(client: FlaskClient):
    player_a = {"name": "Player A", "deck_id": EXAMPLE_DECK_ID}
    player_b = {"name": "Player B", "deck_id": EXAMPLE_DECK_ID}

    response = client.post("/game/start", json={"players": [player_a, player_b]})

    assert response.status_code == 201
    body = response.get_json()
    assert body["active"] is True

    turn_response = client.get(f"/game/{body['game_id']}/active-player")
    assert turn_response.status_code == 200
    assert turn_response.get_json()["active_player_id"] == body["active_player_id"]


def start_state(client):
    response = client.post(
        "/game/start",
        json={
            "players": [
                {"name": "Alice", "deck_id": EXAMPLE_DECK_ID},
                {"name": "Bob", "deck_id": EXAMPLE_DECK_ID},
            ]
        },
    )
    game_id = response.get_json()["game_id"]
    response = client.get(f"/game/{game_id}")
    assert response.status_code == 200
    return response.get_json()


def test_play_and_end_turn(client):
    state = start_state(client)
    path = f"/game/{state['game_id']}"
    player, opponent = state["players"]
    card = next(
        card for card in player["cards_in_hand"] if card["card_type"] == "character"
    )
    payload = {"player_id": player["id"], "card_id": card["id"]}
    response = client.post(path + "/play-card", json=payload)
    assert response.status_code == 200
    played = response.get_json()["players"][0]
    assert len(played["cards_in_hand"]) == len(player["cards_in_hand"]) - 1
    assert played["table"][0]["id"] == card["id"]
    assert played["table"][0]["can_attack"] is False
    assert (
        client.post(
            path + "/play-card",
            json={
                **payload,
                "card_id": player["cards_in_hand"][1]["id"],
            },
        ).status_code
        == 400
    )

    response = client.post(path + "/end-turn", json=payload)
    state = response.get_json()
    assert state["active_player_id"] == opponent["id"]
    assert state["players"][0]["table"][0]["can_attack"] is True
    assert state["players"][1]["hp"] == opponent["hp"]
    assert client.post(path + "/end-turn", json=payload).status_code == 400
    client.post(path + "/end-turn", json={"player_id": opponent["id"]})
    state = client.post(path + "/end-turn", json=payload).get_json()
    assert state["players"][1]["hp"] == opponent["hp"] - card["atk"]

    for _ in range(20):
        if not state["active"]:
            break
        state = client.post(
            path + "/end-turn",
            json={
                "player_id": state["active_player_id"],
            },
        ).get_json()
    assert state["active"] is False
    assert state["winner_id"] == player["id"]
    assert client.post(path + "/end-turn", json=payload).status_code == 400
    assert client.post(path + "/play-card", json=payload).status_code == 400


def test_invalid_moves_do_not_change_state(client):
    state = start_state(client)
    path = f"/game/{state['game_id']}"
    player, opponent = state["players"]
    for payload in (
        {},
        {"player_id": "invalid"},
        {
            "player_id": opponent["id"],
            "card_id": opponent["cards_in_hand"][0]["id"],
        },
        {"player_id": player["id"]},
        {"player_id": player["id"], "card_id": "missing"},
        {
            "player_id": player["id"],
            "card_id": opponent["cards_in_hand"][0]["id"],
        },
    ):
        assert client.post(path + "/play-card", json=payload).status_code == 400
    assert client.post(path + "/end-turn", json=[]).status_code == 400
    assert client.get(path).get_json() == state


def test_missing_game(client):
    from uuid import uuid4

    path = f"/game/{uuid4()}"
    assert client.get(path).status_code == 404
    for action in ("play-card", "end-turn"):
        assert (
            client.post(
                path + "/" + action,
                json={
                    "player_id": str(uuid4()),
                    "card_id": "missing",
                },
            ).status_code
            == 404
        )


def test_start_game_rejects_invalid_deck_uuid(client):
    for deck_id in ("a", "not-a-uuid", "", "../deck_a", None, 123):
        response = client.post(
            "/game/start",
            json={
                "players": [
                    {"name": "Alice", "deck_id": deck_id},
                    {"name": "Bob", "deck_id": EXAMPLE_DECK_ID},
                ]
            },
        )
        assert response.status_code == 400
        assert response.get_json()["errors"][0]["loc"] == ["deck_id"]


def test_start_game_reports_unknown_deck_uuid(client):
    response = client.post(
        "/game/start",
        json={
            "players": [
                {
                    "name": "Alice",
                    "deck_id": "00000000-0000-0000-0000-000000000000",
                },
                {"name": "Bob", "deck_id": EXAMPLE_DECK_ID},
            ]
        },
    )
    assert response.status_code == 400
    assert "not found" in response.get_json()["error"]


def test_start_game_normalizes_deck_uuid(client):
    response = client.post(
        "/game/start",
        json={
            "players": [
                {"name": "Alice", "deck_id": EXAMPLE_DECK_ID.upper()},
                {"name": "Bob", "deck_id": EXAMPLE_DECK_ID},
            ]
        },
    )
    assert response.status_code == 201


def test_turn_draws_and_full_table_rejects_card_without_changing_state(client):
    state = start_state(client)
    path = f"/game/{state['game_id']}"
    assert len(state["players"][0]["cards_in_hand"]) == 6
    assert state["players"][0]["deck_count"] == 9
    assert len(state["players"][1]["cards_in_hand"]) == 5
    assert state["players"][1]["deck_count"] == 10

    # Keep both heroes alive so five full rounds can be exercised via HTTP.
    from uuid import UUID

    game = client.application.extensions["game_service"].get_game(
        UUID(state["game_id"])
    )
    for player in game.players:
        player.hp = 1000
    # Supply characters explicitly: the example deck now also contains items.
    from domain.card import Card, CardType

    game.player_a.cards_in_hand = [
        Card(hp=5, atk=1, name=f"Character {n}", card_type=CardType.CHARACTER)
        for n in range(6)
    ]
    state = client.get(path).get_json()

    for _ in range(5):
        player = state["players"][0]
        response = client.post(
            path + "/play-card",
            json={
                "player_id": player["id"],
                "card_id": next(
                    card["id"]
                    for card in player["cards_in_hand"]
                    if card["card_type"] == "character"
                ),
            },
        )
        assert response.status_code == 200
        for player_id in (game.player_a.id, game.player_b.id):
            response = client.post(
                path + "/end-turn",
                json={
                    "player_id": str(player_id),
                },
            )
            assert response.status_code == 200
        state = response.get_json()

    player = state["players"][0]
    assert len(player["table"]) == 5
    assert player["can_play_card"] is False
    response = client.post(
        path + "/play-card",
        json={
            "player_id": player["id"],
            "card_id": next(
                card["id"]
                for card in player["cards_in_hand"]
                if card["card_type"] == "character"
            ),
        },
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "The table is full (maximum of 5 cards)."
    assert client.get(path).get_json() == state


def test_item_target_validation_and_serialization(client):
    from uuid import UUID
    from domain.card import Card, CardType

    state = start_state(client)
    path = f"/game/{state['game_id']}"
    game = client.application.extensions["game_service"].get_game(
        UUID(state["game_id"])
    )
    target = Card(hp=5, atk=3, name="Target", card_type=CardType.CHARACTER)
    target.activate()
    equipment = Card(
        hp=0,
        atk=0,
        name="Curse",
        card_type=CardType.ITEM,
        hp_modifier=-1,
        atk_modifier=-2,
        deactivate=True,
    )
    game.player_b.table = [target]
    game.player_a.cards_in_hand = [equipment]
    payload = {"player_id": str(game.player_a.id), "card_id": equipment.id}
    before = client.get(path).get_json()
    for invalid in (None, "", 123, [], {}, "missing"):
        response = client.post(
            path + "/play-card", json={**payload, "target_card_id": invalid}
        )
        assert response.status_code == 400
        assert client.get(path).get_json() == before
    response = client.post(
        path + "/play-card", json={**payload, "target_card_id": target.id}
    )
    assert response.status_code == 200
    result = response.get_json()
    assert result["players"][0]["cards_in_hand"] == []
    assert result["players"][0]["can_play_item"] is False
    applied = result["players"][1]["table"][0]
    assert (applied["hp"], applied["atk"], applied["can_attack"]) == (4, 1, False)
    assert applied["items"][0]["id"] == equipment.id
    assert applied["items"][0]["deactivate"] is True
