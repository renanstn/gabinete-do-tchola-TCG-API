import uuid
from typing import List, Optional

from api.game.card import Card


class Player:
    """
    Um jogador, possui um deck de cartas e faz ações de baixr cartas na mesa.
    """

    def __init__(self, name: str, deck: List[Card]):
        self.id = uuid.uuid4()
        self.name = name
        self.hp = 10
        self.deck = deck
        self.cards_in_hand = []
        self.table: List[Card] = []

    def draw_card(self):
        if len(self.deck):
            drawn_card = self.deck.pop()
            print(f"Drawn card: {drawn_card}")
            self.cards_in_hand.append(drawn_card)
        else:
            print("No more cards to draw")

    def play_card(self, card_id: str):
        """
        Registra uma carta jogada na mesa pelo jogador.
        - Insere o card na table list.
        """
        pass
