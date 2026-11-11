"""Mapeamento privado de persistência, independente dos schemas HTTP."""

from typing import Any
from uuid import UUID

from domain.card import Card, CardType, CharacterCard, ItemCard, StageCard
from domain.game import Game
from domain.player import Player


def _card_to_dict(card: Card) -> dict[str, Any]:
    data = {
        "id": card.id,
        "name": card.name,
        "card_type": card.card_type.value,
        "description": card.description,
        "image": card.image,
        "sound": card.sound,
    }
    if isinstance(card, CharacterCard):
        data.update(
            hp=card.hp,
            initial_hp=card.initial_hp,
            atk=card.atk,
            can_attack=card.can_attack,
            items=[_card_to_dict(item) for item in card.items],
        )
    elif isinstance(card, ItemCard):
        data.update(
            hp_modifier=card.hp_modifier,
            atk_modifier=card.atk_modifier,
            deactivate=card.deactivate,
            hp_set=card.hp_set,
            atk_set=card.atk_set,
        )
    return data


def _card_from_dict(data: dict[str, Any]) -> Card:
    # Version 1 snapshots also contain unused fields; only read fields for this type.
    common = {key: data[key] for key in ("id", "name", "description", "image", "sound")}
    card_type = CardType(data["card_type"])
    if card_type == CardType.CHARACTER:
        card = CharacterCard(hp=data["hp"], atk=data["atk"], **common)
        card.initial_hp = data["initial_hp"]
        card.can_attack = data["can_attack"]
        items = [_card_from_dict(item) for item in data["items"]]
        if any(not isinstance(item, ItemCard) for item in items):
            raise ValueError("Character equipment must contain only items.")
        # Effects are already reflected in the saved combat state.
        card.items = items
        return card
    if card_type == CardType.ITEM:
        return ItemCard(
            hp_modifier=data["hp_modifier"],
            atk_modifier=data["atk_modifier"],
            deactivate=data["deactivate"],
            hp_set=data.get("hp_set"),
            atk_set=data.get("atk_set"),
            **common
        )
    return StageCard(**common)


def _player_to_dict(player: Player) -> dict[str, Any]:
    return {
        "id": str(player.id),
        "name": player.name,
        "hp": player.hp,
        "has_played_card": player.has_played_card,
        **{
            zone: [_card_to_dict(card) for card in getattr(player, zone)]
            for zone in ("deck", "cards_in_hand", "table", "cemetery")
        },
    }


def _player_from_dict(data: dict[str, Any]) -> Player:
    player = Player(data["name"], [])
    player.id = UUID(data["id"])
    player.hp = data["hp"]
    player.has_played_card = data["has_played_card"]
    for zone in ("deck", "cards_in_hand", "table", "cemetery"):
        setattr(player, zone, [_card_from_dict(card) for card in data[zone]])
    return player


def game_to_snapshot(game: Game) -> dict[str, Any]:
    return {
        "version": 2,
        "id": str(game.id),
        "players": [_player_to_dict(player) for player in game.players],
        "active_player_id": str(game.active_player_id),
        "active": game.active,
        "winner_id": str(game.winner.id) if game.winner else None,
    }


def game_from_snapshot(data: dict[str, Any]) -> Game:
    if data["version"] not in (1, 2):
        raise ValueError("Unsupported game snapshot version.")
    player_a, player_b = [_player_from_dict(p) for p in data["players"]]
    game = Game(player_a, player_b)
    game.id = UUID(data["id"])
    game.active_player_id = UUID(data["active_player_id"])
    game.active = data["active"]
    if data["winner_id"] is not None:
        game.winner = next(p for p in game.players if str(p.id) == data["winner_id"])
    return game
