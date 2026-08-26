from src.shared.domain.entities.project import Project
import uuid


class ProjectDynamoDTO:
    title: str
    description: str
    associates: list[uuid.UUID]
    display_image: str
    id: uuid.UUID

    def __init__(self, title: str, description: str, associates: list[uuid.UUID], display_image: str, id: uuid.UUID):
        self.title = title
        self.description = description
        self.associates = associates
        self.display_image = display_image
        self.id = id

    @staticmethod
    def from_entity(project: Project) -> "ProjectDynamoDTO":
        """
        Parse data from Project to ProjectDynamoDTO
        """
        return ProjectDynamoDTO(
            title=project.title,
            description=project.description,
            associates=project.associates,
            display_image=project.display_image,
            id=project.id
        )

    def to_dynamo(self) -> dict:
        """
        Parse data from ProjectDynamoDTO to dict
        """
        return {
            "entity": "project",
            "title": self.title,
            "description": self.description,
            "associates": [str(associate) for associate in self.associates] if self.associates else [],
            "display_image": self.display_image,
            "id": str(self.id),
        }

    @staticmethod
    def from_dynamo(project_data: dict) -> "ProjectDynamoDTO":
        """
        Parse data from DynamoDB to ProjectDynamoDTO
        @param project_data: dict from DynamoDB
        """
        associates = project_data.get("associates")
        return ProjectDynamoDTO(
            title=project_data["title"],
            description=project_data["description"],
            associates=[uuid.UUID(associate) for associate in associates] if associates else None,
            display_image=project_data.get("display_image"),
            id=uuid.UUID(project_data["id"])
        )

    def to_entity(self) -> Project:
        """
        Parse data from ProjectDynamoDTO to Project
        """
        return Project(
            title=self.title,
            description=self.description,
            associates=self.associates,
            display_image=self.display_image,
            id=self.id
        )

    def __repr__(self):
        return f"ProjectDynamoDto(title={self.title}, description={self.description}, associates={self.associates}, display_image={self.display_image}, id={self.id})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__