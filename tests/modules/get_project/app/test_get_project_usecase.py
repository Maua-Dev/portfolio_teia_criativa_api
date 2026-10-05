import uuid

import pytest

from src.modules.get_project.app.get_project_usecase import GetProjectUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_GetProjectUsecase:

    def test_get_project(self):
        repo = ProjectRepositoryMock()
        observability = ObservabilityMock(module_name="get_project")
        usecase = GetProjectUsecase(repo, observability=observability)

        existing_project_id = repo.projects[1].id

        project = usecase(project_id=existing_project_id)

        assert project.id == existing_project_id

    def test_get_project_not_found(self):
        repo = ProjectRepositoryMock()
        observability = ObservabilityMock(module_name="get_project")
        usecase = GetProjectUsecase(repo, observability=observability)

        with pytest.raises(NoItemsFound):
            usecase(project_id=uuid.uuid4())

    def test_get_project_invalid_id(self):
        repo = ProjectRepositoryMock()
        observability = ObservabilityMock(module_name="get_project")
        usecase = GetProjectUsecase(repo, observability=observability)

        with pytest.raises(EntityError):
            usecase(project_id="invalid")