class DomainError(Exception):
    """Erro esperado ao aplicar uma regra do jogo."""


class InvalidMoveError(DomainError):
    """A jogada viola uma regra do jogo."""
