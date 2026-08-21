from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StartGamePlayer:
    name: str
    deck_id: str
