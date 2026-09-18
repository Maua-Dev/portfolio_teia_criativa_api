import uuid

from src.shared.domain.entities.project import Project
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    strip_keys,
    PK_ATTR,
    SK_ATTR
)


class ProjectDynamoDTO:

    @staticmethod
    def from_entity_to_dynamo(project: Project) -> dict:
        return {
            PK_ATTR: partition_key(kind=EntityKind.PROJECT),
            SK_ATTR: sort_key(id=project.id, kind=EntityKind.PROJECT),
            "id": str(project.id),
            "title": project.title,
            "description": project.description,
            "associates": [str(associate) for associate in project.associates] if project.associates else [],
            "display_image": project.display_image
        }

    @staticmethod
    def from_dynamo_to_entity(project_data: dict) -> Project:
        return Project.model_validate(obj=strip_keys(project_data))