from adapters.repositories.models.card import Card as CardModel
from domain.card import Card as CardDomain


def model_to_domain(model: CardModel) -> CardDomain:
    return CardDomain(
        id=model.id,
        name=model.name,
        description=model.description,
        attack=model.attack,
        defense=model.defense,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def domain_to_model(domain: CardDomain) -> CardModel:
    return CardModel(
        id=domain.id,
        name=domain.name,
        description=domain.description,
        attack=domain.attack,
        defense=domain.defense,
        created_at=domain.created_at,
        updated_at=domain.updated_at,
    )
