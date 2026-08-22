from adapters.repositories.in_memory_game_repository import \
    InMemoryGameRepository
from application.commands import StartGamePlayer
from application.game_service import GameService
from application.ports.deck_repository import DeckRepository
from domain.card import Card, CardType


class FakeDeckRepository(DeckRepository):
    def get_cards(self, deck_id: str) -> list[Card]:
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
            StartGamePlayer(name="A", deck_id="first"),
            StartGamePlayer(name="B", deck_id="second"),
        ]
    )

    assert games.get_by_id(game.id) is game
    assert game.active_player_id == game.player_a.id
    assert len(game.player_a.cards_in_hand) == 5
    assert len(game.player_b.cards_in_hand) == 5
