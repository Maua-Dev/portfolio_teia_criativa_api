from typing import List
import uuid

from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class ProjectRepositoryMock(IProjectRepository):
    projects: List[Project]
    projects_counter: int

    def __init__(self):
        self.projects = [
            Project(title="Teia Criativa", description="Projeto inicial de exemplo"),
            Project(title="Portfolio Pessoal", description="Site pessoal com projetos acadêmicos"),
            Project(title="Sistema de Agenda", description="Aplicativo desktop de agenda"),
        ]
        self.projects_counter = 3

    def get_project(self, project_id: uuid.UUID) -> Project:
        for project in self.projects:
            if project.id == project_id:
                return project
        raise NoItemsFound("project_id")

    def get_all_project(self) -> List[Project]:
        return self.projects

    def create_project(self, new_project: Project) -> Project:
        self.projects.append(new_project)
        self.projects_counter += 1
        return new_project

    def delete_project(self, project_id: uuid.UUID) -> Project:
        for idx, project in enumerate(self.projects):
            if project.id == project_id:
                return self.projects.pop(idx)
        raise NoItemsFound("project_id")

    def update_project(self, project_id: uuid.UUID, new_title: str) -> Project:
        for project in self.projects:
            if project.id == project_id:
                project.title = new_title
                return project
        raise NoItemsFound("project_id")
    
    def get_project_counter(self) -> int:
            return self.projects_counter