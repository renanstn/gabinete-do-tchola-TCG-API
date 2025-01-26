import uuid
from typing import List

from api.domain.card import Card


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
        self.cemetery = []

    def draw_card(self):
        if len(self.deck):
            drawn_card = self.deck.pop()
            print(f"Player {self.name} drawn card: {drawn_card.id}")
            self.cards_in_hand.append(drawn_card)
        else:
            print("No more cards to draw")

    def play_card(self, card_id: str):
        """
        Registra uma carta jogada na mesa pelo jogador.
        - Insere o card na table list.
        """
        if not self.can_play_card():
            print("This player already made its play")
            return
        selected_card = self.get_card_by_id(card_id)
        self.remove_card_from_hand(selected_card.id)
        self.table.append(selected_card)
        print(f"Player {self.name} play a card")

    def is_alive(self) -> bool:
        return self.hp > 0

    def has_cards_on_table(self):
        return len(self.table) > 0

    def get_card_by_id(self, card_id: str) -> Card:
        for card in self.cards_in_hand:
            if card.id == card_id:
                return card
        raise Exception(
            f"Player {self.name} don't have any card with ID {card_id}"
        )

    def remove_card_from_hand(self, card_id: str):
        self.cards_in_hand = [
            card for card in self.cards_in_hand if card.id != card_id
        ]

    def remove_card_from_table(self, card_id: str):
        self.table = [card for card in self.table if card.id != card_id]

    def subtract_life(self, ammount: int):
        self.hp -= ammount

    def move_card_to_cemetery(self, card: Card):
        self.remove_card_from_table(card.id)
        self.cemetery.append(card)

    def can_play_card(self) -> bool:
        return not any(card for card in self.table if card.can_attack is False)
