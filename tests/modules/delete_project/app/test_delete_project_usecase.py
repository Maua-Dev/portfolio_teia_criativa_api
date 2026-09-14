import uuid

import pytest

from src.modules.delete_project.app.delete_project_usecase import DeleteProjectUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_DeleteProjectUsecase:

    def test_delete_project(self):
        repo = ProjectRepositoryMock()
        usecase = DeleteProjectUsecase(repo)

        lenBefore = len(repo.projects)
        existing_project_id = repo.projects[0].id

        project = usecase(existing_project_id)

        assert len(repo.projects) == lenBefore - 1
        assert project.id == existing_project_id

    def test_delete_project_not_found(self):
        repo = ProjectRepositoryMock()
        usecase = DeleteProjectUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(uuid.uuid4())

    def test_delete_project_invalid_id(self):
        repo = ProjectRepositoryMock()
        usecase = DeleteProjectUsecase(repo)

        with pytest.raises(EntityError):
            usecase("invalid")