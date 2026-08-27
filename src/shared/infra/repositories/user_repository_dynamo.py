from typing import List
import uuid

from boto3.dynamodb.conditions import Key
import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource

from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    PK_ATTR,
    SK_ATTR
)


class UserRepositoryDynamo(IUserRepository):

    @pytest.marskip("tests cant run in gh actions")
    def __init__(self):
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            dynamo_table_name=envs.dynamo_table_name,
            region=envs.region,
            partition_key=envs.dynamo_partition_key,
            sort_key=envs.dynamo_sort_key,
            endpoint_url=envs.dynamo_endpoint_url,
        )

    @pytest.marskip("tests cant run in gh actions")
    def _pk(self) -> str:
        return partition_key(kind=EntityKind.USER)

    @pytest.marskip("tests cant run in gh actions")
    def _sk(self, user_id: uuid.UUID) -> str:
        return sort_key(id=user_id, kind=EntityKind.USER)

    @pytest.marskip("tests cant run in gh actions")
    def get_user(self, user_id: uuid.UUID) -> User:
        resp = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if "Item" not in resp:
            raise NoItemsFound("user_id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Item"])

    @pytest.marskip("tests cant run in gh actions")
    def get_all_user(self) -> List[User]:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
        )

        return [
            UserDynamoDTO.from_dynamo_to_entity(item)
            for item in resp.get("Items", [])
        ]

    @pytest.marskip("tests cant run in gh actions")
    def create_user(self, new_user: User) -> User:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(new_user.id),
        )
        if "Item" in existing:
            raise DuplicatedItem("user_id")

        item_to_put = UserDynamoDTO.from_entity_to_dynamo(new_user)
        self.dynamo.put_item(
            item=item_to_put,
            partition_key=self._pk(),
            sort_key=self._sk(new_user.id),
        )
        return new_user

    @pytest.marskip("tests cant run in gh actions")
    def delete_user(self, user_id: uuid.UUID) -> User:
        resp = self.dynamo.delete_item(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if "Attributes" not in resp:
            raise NoItemsFound("user_id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Attributes"])

    @pytest.marskip("tests cant run in gh actions")
    def update_user(self, updated_user: User) -> User:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(updated_user.id),
        )
        if "Item" not in existing:
            raise NoItemsFound("user_id")

        item_to_put = UserDynamoDTO.from_entity_to_dynamo(updated_user)
        self.dynamo.put_item(
            item=item_to_put,
            partition_key=self._pk(),
            sort_key=self._sk(updated_user.id),
        )
        return updated_user