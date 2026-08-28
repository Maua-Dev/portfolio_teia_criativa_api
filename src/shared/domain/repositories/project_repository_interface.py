from abc import ABC, abstractmethod
from typing import Optional
import uuid

from src.shared.domain.entities.project import Project


class IProjectRepository(ABC):
    @abstractmethod
    def create_project(self, project: Project) -> Project:
        pass

    @abstractmethod
    def get_project(self, project_id: uuid.UUID) -> Optional[Project]:
        pass

    @abstractmethod
    def get_all_project(self) -> list[Project]:
        pass

    @abstractmethod
    def update_project(self, project: Project) -> Optional[Project]:
        pass

    @abstractmethod
    def delete_project(self, project_id: uuid.UUID) -> bool:
        pass