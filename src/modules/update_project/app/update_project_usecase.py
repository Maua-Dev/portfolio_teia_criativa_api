from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.helpers.errors.domain_errors import EntityError
import uuid

class UpdateProjectUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self, project_id: int, new_title: str, new_description: str) -> Project:

        if type(project_id) != uuid.UUID:
            raise EntityError("project_id")
        
        if type(new_title) != str:
            raise EntityError("new_title")

        if type(new_description) != str:
            raise EntityError('new_description')

        updated_project = self.repo.update_project(project_id=project_id, new_title=new_title, new_description=new_description)

        return updated_project
