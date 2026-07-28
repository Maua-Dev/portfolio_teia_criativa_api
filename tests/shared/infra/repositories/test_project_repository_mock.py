import uuid
import pytest

from src.shared.domain.entities.project import Project
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_ProjectRepositoryMock:
    def test_get_project(self):
        repo = ProjectRepositoryMock()
        projeto_existente = repo.projects[0]

        project = repo.get_project(projeto_existente.id)

        assert project.title == "Teia criativa"
        assert project.description == "Projeto inicial de exemplo"

    def test_get_project_not_found(self):
        repo = ProjectRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_project(uuid.uuid4())

    def test_get_all_project(self):
        repo = ProjectRepositoryMock()
        projects = repo.get_all_project()
        assert len(projects) == 3

    def test_create_project(self):
        repo = ProjectRepositoryMock()
        project = Project(
            title="Novo projeto",
            description="Projeto criado no teste"
        )

        repo.create_project(project)

        assert repo.projects[3].title == "Novo projeto"
        assert repo.projects[3].description == "Projeto criado no teste"

        assert repo.projects_counter == 4

    def test_delete_project(self):
        repo = ProjectRepositoryMock()
        projeto_existente = repo.projects[0]

        project = repo.delete_project(projeto_existente.id)

        assert project.title == "Teia criativa"
        assert project.description == "Projeto inicial de exemplo"

    def test_delete_project_not_found(self):
        repo = ProjectRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.delete_project(uuid.uuid4())

    def test_update_project(self):
        repo = ProjectRepositoryMock()
        projeto_existente = repo.projects[0]

        project = repo.update_project(projeto_existente.id, "Teia Criativa Renovada")

        assert project.title == "Teia Criativa Renovada"
        assert repo.projects[0].title == "Teia Criativa Renovada"

    def test_update_project_not_found(self):
        repo = ProjectRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.update_project(uuid.uuid4(), "Teia Criativa Renovada")

    def test_get_projects_counter(self):
        repo = ProjectRepositoryMock()
        assert repo.get_project_counter() == 3