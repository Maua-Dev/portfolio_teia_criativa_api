import uuid
from src.shared.domain.entities.user import User
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    strip_keys,
    PK_ATTR,
    SK_ATTR
)


class UserDynamoDTO:

    @staticmethod
    def from_entity_to_dynamo(user: User) -> dict:
        return {
            PK_ATTR: partition_key(kind=EntityKind.USER),
            SK_ATTR: sort_key(id=user.id, kind=EntityKind.USER),
            "id": str(user.id),
            "email": user.email,
            "role": user.role.value if hasattr(user.role, 'value') else str(user.role),
            "active": user.active,
            "user_name": user.user_name
        }

    @staticmethod
    def from_dynamo_to_entity(user_data: dict) -> User:
        return User.model_validate(obj=strip_keys(user_data))