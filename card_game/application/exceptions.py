class ApplicationError(Exception):
    """Erro esperado na execução de um caso de uso."""


class GameNotFoundError(ApplicationError):
    pass


class InvalidGameSetupError(ApplicationError):
    pass


class DeckNotFoundError(ApplicationError):
    pass
