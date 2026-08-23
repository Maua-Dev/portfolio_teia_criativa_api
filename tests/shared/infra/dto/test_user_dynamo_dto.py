import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.external.dynamo.dynamo_keys import EntityKind, PK_ATTR, SK_ATTR


class Test_UserDynamoDTO:
    def test_from_entity_to_dynamo(self):
        user = User(
            id=uuid.uuid4(),
            email="teste@teste.com",
            senha_hash="hash123",
            role=RoleEnum.USER
        )

        dynamo_dict = UserDynamoDTO.from_entity_to_dynamo(user)

        assert dynamo_dict[PK_ATTR] == EntityKind.USER.value
        assert dynamo_dict[SK_ATTR] == f"USER#{user.id}"
        assert dynamo_dict["email"] == user.email
        assert dynamo_dict["role"] == user.role.value

    def test_from_dynamo_to_entity_roundtrip(self):
        user = User(
            id=uuid.uuid4(),
            email="teste@teste.com",
            senha_hash="hash123",
            role=RoleEnum.USER
        )

        dynamo_dict = UserDynamoDTO.from_entity_to_dynamo(user)
        entity = UserDynamoDTO.from_dynamo_to_entity(dynamo_dict)

        assert entity.id == user.id
        assert entity.email == user.email
        assert entity.role == user.role