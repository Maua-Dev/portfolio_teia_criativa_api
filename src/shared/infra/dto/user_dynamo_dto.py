from src.shared.domain.entities.user import User
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    strip_keys,
)


class UserDynamoDTO:

    @staticmethod
    def from_entity_to_dynamo(user: User) -> dict:
        """
        Converts an user entity to a dictionary compatible with DynamoDB.

        Includes base keys (pk/sk).

        Args:
            user: The user entity to serialize.

        Returns:
            Dict as expected by DynamoDB put_user.
        """
        return {
            **user.model_dump(mode="json"),
            "pk": partition_key(kind=EntityKind.User),
            "sk": sort_key(id=user.id, kind=EntityKind.User),
        }

    @staticmethod
    def from_dynamo_to_entity(user_data: dict) -> User:
        """
        Converts a DynamoDB user dict into an user entity.

        Args:
            user_data: Dictionary from DynamoDB.

        Returns:
            user entity with storage keys removed.
        """
        return User.model_validate(obj=strip_keys(user_data))
