from typing import List
import uuid

from boto3.dynamodb.conditions import Key
import pytest
from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.dto.member_dynamo_dto import MemberDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource

from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    PK_ATTR,
    SK_ATTR
)


class MemberRepositoryDynamo(IMemberRepository):

    @pytest.mark.skip("tests cant run in gh actions")
    def __init__(self):
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            dynamo_table_name=envs.dynamo_table_name,
            region=envs.region,
            partition_key=envs.dynamo_partition_key,
            sort_key=envs.dynamo_sort_key,
            endpoint_url=envs.dynamo_endpoint_url,
        )

    @pytest.mark.skip("tests cant run in gh actions")
    def _pk(self) -> str:
        return partition_key(kind=EntityKind.MEMBER)

    @pytest.mark.skip("tests cant run in gh actions")
    def _sk(self, user_id: uuid.UUID) -> str:
        return sort_key(id=user_id, kind=EntityKind.MEMBER)

    @pytest.mark.skip("tests cant run in gh actions")
    def get_all_members(self) -> List[Member]:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
        )

        return [
            MemberDynamoDTO.from_dynamo_to_entity(item)
            for item in resp.get("Items", [])
        ]

    @pytest.mark.skip("tests cant run in gh actions")
    def create_member(self, new_member: Member) -> Member:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(new_member.member_id),
        )
        if "Item" in existing:
            raise DuplicatedItem("member")

        item_to_put = MemberDynamoDTO.from_entity_to_dynamo(new_member)
        self.dynamo.put_item(
            item=item_to_put,
            partition_key=self._pk(),
            sort_key=self._sk(new_member.member_id),
        )
        return new_member
