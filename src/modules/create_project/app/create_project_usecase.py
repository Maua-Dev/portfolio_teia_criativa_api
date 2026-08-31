from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.helpers.errors.domain_errors import EntityError
import uuid
from typing import Optional

class CreateProjectUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self, title: str, description: str, associates: Optional[list[uuid.UUID]], display_image: Optional[str]) -> Project:

        project = Project(
            title=title,
            description=description,
            associates=associates,
            display_image=display_image
        )

        return self.repo.create_project(project)