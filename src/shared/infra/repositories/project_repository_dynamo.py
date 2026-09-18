from typing import List
import uuid

from boto3.dynamodb.conditions import Key
import pytest
from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound
from src.shared.infra.dto.project_dynamo_dto import ProjectDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource

from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    PK_ATTR,
    SK_ATTR
)


class ProjectRepositoryDynamo(IProjectRepository):

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
        return partition_key(kind=EntityKind.PROJECT)

    @pytest.mark.skip("tests cant run in gh actions")
    def _sk(self, project_id: uuid.UUID) -> str:
        return sort_key(id=project_id, kind=EntityKind.PROJECT)

    @pytest.mark.skip("tests cant run in gh actions")
    def get_project(self, project_id: uuid.UUID) -> Project:
        resp = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(project_id),
        )

        if "Item" not in resp:
            raise NoItemsFound("project_id")

        return ProjectDynamoDTO.from_dynamo_to_entity(resp["Item"])

    @pytest.mark.skip("tests cant run in gh actions")
    def get_all_project(self) -> List[Project]:
        resp = self.dynamo.query(
            key_condition_expression=Key(PK_ATTR).eq(self._pk()),
        )

        return [
            ProjectDynamoDTO.from_dynamo_to_entity(item)
            for item in resp.get("Items", [])
        ]

    @pytest.mark.skip("tests cant run in gh actions")
    def create_project(self, new_project: Project) -> Project:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(new_project.id),
        )
        if "Item" in existing:
            raise DuplicatedItem("project_id")

        item_to_put = ProjectDynamoDTO.from_entity_to_dynamo(new_project)
        self.dynamo.put_item(
            item=item_to_put,
            partition_key=self._pk(),
            sort_key=self._sk(new_project.id),
        )
        return new_project

    @pytest.mark.skip("tests cant run in gh actions")
    def delete_project(self, project_id: uuid.UUID) -> Project:
        resp = self.dynamo.delete_item(
            partition_key=self._pk(),
            sort_key=self._sk(project_id),
        )

        if "Attributes" not in resp:
            raise NoItemsFound("project_id")

        return ProjectDynamoDTO.from_dynamo_to_entity(resp["Attributes"])

    @pytest.mark.skip("tests cant run in gh actions")
    def update_project(self, project: Project) -> Project:
        existing = self.dynamo.get_item(
            partition_key=self._pk(),
            sort_key=self._sk(project.id),
        )
        if "Item" not in existing:
            raise NoItemsFound("project_id")

        item_to_put = ProjectDynamoDTO.from_entity_to_dynamo(project)
        self.dynamo.put_item(
            item=item_to_put,
            partition_key=self._pk(),
            sort_key=self._sk(project.id),
        )
        return project