from uuid import UUID

from adapters.repositories.in_memory_game_repository import (
    InMemoryGameRepository,
)
from application.commands import StartGamePlayer
from application.game_service import GameService
from application.ports.deck_repository import DeckRepository
from domain.card import Card, CardType


class FakeDeckRepository(DeckRepository):
    def get_cards(self, deck_id: UUID) -> list[Card]:
        return [
            Card(
                hp=1,
                atk=1,
                name=f"{deck_id}-{number}",
                card_type=CardType.CHARACTER,
            )
            for number in range(5)
        ]


def test_start_game_uses_ports_and_sets_up_the_domain_game():
    games = InMemoryGameRepository()
    service = GameService(games, FakeDeckRepository())

    game = service.start_game(
        [
            StartGamePlayer(
                name="A", deck_id=UUID("6c2e32a4-644d-4be5-bd8a-62b683b08757")
            ),
            StartGamePlayer(
                name="B", deck_id=UUID("a2a10a78-4276-4538-98a7-8a89c49c9aa5")
            ),
        ]
    )

    assert games.get_by_id(game.id) is game
    assert game.active_player_id == game.player_a.id
    assert len(game.player_a.cards_in_hand) == 5
    assert len(game.player_b.cards_in_hand) == 5
