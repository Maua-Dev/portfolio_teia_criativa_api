from typing import List

import uuid

from boto3.dynamodb.conditions import Key
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import DuplicatedUser, NoUsersFound
from src.shared.infra.dto.template_dynamo_dto import ItemDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource

from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    PK_ATTR,
    SK_ATTR
)


class TemplateRepositoryDynamo(IUserRepository):

    def __init__(self):
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            dynamo_table_name=envs.dynamo_table_name,
            region=envs.region,
            partition_key=envs.dynamo_partition_key,
            sort_key=envs.dynamo_sort_key,
            endpoint_url=envs.dynamo_endpoint_url,
        )

    def _pk(self) -> str:
        return partition_key(kind=EntityKind.User)

    def _sk(self, user_id: UUID) -> str:
        return sort_key(id=uuid.UUID(user_id), kind=EntityKind.User)

    def get_user(self, user_id: UUID) -> User:
        resp = self.dynamo.get_user(
            partition_key=self._pk(),
            sort_key=self._sk(user_id),
        )

        if resp.get("User") is None:
            raise NoUsersFound(user_id)

        return ItemDynamoDTO.from_dynamo_to_entity(resp[User])

    def get_all_User(self) -> List[User]:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
        )

        return [
            UserDynamoDTO.from_dynamo_to_entity(User)
            for User in resp.get("Users", [])
        ]

    def create_User(self, new_User: User) -> User:
        existing = self.dynamo.get_User(
            partition_key=self._pk(),
            sort_key=self._sk(new_User.User_id),
        )
        if existing.get("User") is not None:
            raise DuplicatedUser("User_id")

        self.dynamo.put_User(
            User=UserDynamoDTO.from_entity_to_dynamo(new_User),
            partition_key=self._pk(),
            sort_key=self._sk(new_User.User_id),
        )
        return new_User

    def delete_User(self, User_id: UUID) -> User:
        resp = self.dynamo.delete_User(
            partition_key=self._pk(),
            sort_key=self._sk(User_id),
        )

        if "Attributes" not in resp:
            raise NoUsersFound("User_id")

        return UserDynamoDTO.from_dynamo_to_entity(resp["Attributes"])

    def update_User(self, updated_User: User) -> User:
        existing = self.dynamo.get_User(
            partition_key=self._pk(),
            sort_key=self._sk(updated_User.User_id),
        )
        if existing.get("User") is None:
            raise NoUsersFound("User_id")

        self.dynamo.put_User(
            User=UserDynamoDTO.from_entity_to_dynamo(updated_User),
            partition_key=self._pk(),
            sort_key=self._sk(updated_User.User_id),
        )
        return updated_User
    
