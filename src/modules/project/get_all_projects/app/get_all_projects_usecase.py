from src.shared.domain.entities.project import Project
from typing import List
from src.shared.domain.repositories.project_repository_interface import IProjectRepository


class GetAllProjectsUsecase:
    def __init__(self, repo: IProjectRepository):
        self.repo = repo

    def __call__(self) -> List[Project]:
        all_projects_list = self.repo.get_all_project()

        return all_projects_list
