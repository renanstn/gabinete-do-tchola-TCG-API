from adapters.repositories.models.player import Player as PlayerModel
from domain.player import Player as PlayerDomain


def model_to_domain(model: PlayerModel) -> PlayerDomain:
    return PlayerDomain(
        id=model.id,
        name=model.name,
        score=model.score,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def domain_to_model(domain: PlayerDomain) -> PlayerModel:
    return PlayerModel(
        id=domain.id,
        name=domain.name,
        score=domain.score,
        created_at=domain.created_at,
        updated_at=domain.updated_at,
    )
