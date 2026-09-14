from src.shared.domain.entities.project import Project
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
import uuid


class GetProjectUsecase:
    def __init__(self, repo: IProjectRepository, observability: ObservabilityAWS):
        self.repo = repo
        self.observability = observability

    def __call__(self, project_id: uuid.UUID) -> Project:
        self.observability.log_usecase_in()
        if type(project_id) != uuid.UUID:
            raise EntityError("project_id")
        project = self.repo.get_project(project_id)
        self.observability.log_usecase_out()
        return project
