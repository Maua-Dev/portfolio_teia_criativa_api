from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.helpers.errors.domain_errors import EntityError

class CreateProjectUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self, title: str, description: str) -> Project:

        project = Project(
            title=title,
            description=description,
        )

        return self.repo.create_project(project)