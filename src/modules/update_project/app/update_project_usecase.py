from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.helpers.errors.domain_errors import EntityError
import uuid
from typing import Optional


class UpdateProjectUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(
        self,
        project_id: uuid.UUID,
        new_title: str,
        new_description: str,
        new_associates: Optional[list[uuid.UUID]] = None,
        new_display_image: Optional[str] = None
    ) -> Project:

        if type(project_id) != uuid.UUID:
            raise EntityError("project_id")

        if type(new_title) != str:
            raise EntityError("new_title")

        if type(new_description) != str:
            raise EntityError('new_description')

        if new_associates is not None and type(new_associates) != list:
            raise EntityError("new_associates")

        if new_display_image is not None and type(new_display_image) != str:
            raise EntityError("new_display_image")

        existing_project = self.repo.get_project(project_id)
        existing_project.title = new_title
        existing_project.description = new_description

        if new_associates is not None:
            existing_project.associates = new_associates

        if new_display_image is not None:
            existing_project.display_image = new_display_image

        updated_project = self.repo.update_project(project=existing_project)

        return updated_project