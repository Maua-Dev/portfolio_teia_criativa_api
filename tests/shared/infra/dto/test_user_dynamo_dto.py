import pytest

pytest.importorskip("src.shared.infra.dto.user_dynamo_dto")

from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserDynamoDTO:
    def test_from_entity_to_dynamo(self):
        user = UserRepositoryMock().users[0]
        data = UserDynamoDTO.from_entity_to_dynamo(user)

        assert data["pk"] == "USER"
        assert data["sk"] == f"USER#{user.id}"
        assert data["email"] == user.email
        assert data["role"] == RoleEnum.ADMIN.value
        assert data["senha_hash"] == user.senha_hash

    def test_from_dynamo_to_entity_roundtrip(self):
        user = UserRepositoryMock().users[1]
        dynamo = UserDynamoDTO.from_entity_to_dynamo(user)
        restored = UserDynamoDTO.from_dynamo_to_entity(dynamo)

        assert restored.id == user.id
        assert restored.email == user.email
        assert restored.role == RoleEnum.USER
        assert restored.senha_hash == user.senha_hash
        assert "pk" not in restored.model_dump()
        assert "sk" not in restored.model_dump()
