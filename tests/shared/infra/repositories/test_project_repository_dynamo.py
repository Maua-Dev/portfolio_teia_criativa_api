import os

import pytest

from src.shared.infra.repositories.project_repository_dynamo import ProjectRepositoryDynamo
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_ProjectRepositoryDynamo:

    def test_create_project(self):
        os.environ["STAGE"] = "TEST"

        project_repository = ProjectRepositoryDynamo()
        project_repository_mock = ProjectRepositoryMock()
        resp = project_repository.create_project(project_repository_mock.projects[0])

        assert project_repository_mock.projects[0].title == resp.title

    def test_get_project(self):
        os.environ["STAGE"] = "TEST"

        project_repository = ProjectRepositoryDynamo()
        project_repository_mock = ProjectRepositoryMock()

        created = project_repository.create_project(project_repository_mock.projects[0])
        resp = project_repository.get_project(created.id)

        assert created.title == resp.title

    def test_delete_project(self):
        os.environ["STAGE"] = "TEST"

        project_repository = ProjectRepositoryDynamo()
        project_repository_mock = ProjectRepositoryMock()

        created = project_repository.create_project(project_repository_mock.projects[2])
        resp = project_repository.delete_project(created.id)

        assert created.title == resp.title

    def test_get_all_project(self):
        os.environ["STAGE"] = "TEST"

        project_repository = ProjectRepositoryDynamo()
        project_repository_mock = ProjectRepositoryMock()

        project_repository.create_project(project_repository_mock.projects[0])
        resp = project_repository.get_all_project()

        assert len(resp) >= 1

    def test_update_project(self):
        os.environ["STAGE"] = "TEST"

        project_repository = ProjectRepositoryDynamo()
        project_repository_mock = ProjectRepositoryMock()

        created = project_repository.create_project(project_repository_mock.projects[0])
        resp = project_repository.update_project(
            project_id=created.id,
            new_title="Novo Título do Projeto"
        )

        assert resp.title == "Novo título do projeto"