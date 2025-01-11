import uuid
from typing import List, Optional


class Player:
    """
    Um jogador, possui um deck de cartas e faz ações de baixr cartas na mesa.
    """

    def __init__(self, name: str):
        self.id = uuid.uuid4()
        self.name = name
        self.hp = 10
        self.cards: List[Card] = []

    def play_card(self, card_id: str):
        """
        Registra uma carta jogada na mesa pelo jogador.
        """
        pass
