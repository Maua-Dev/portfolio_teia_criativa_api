import uuid

import pytest

from src.modules.update_project.app.update_project_usecase import UpdateProjectUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_UpdateProjectUsecase:

    def test_update_project_usecase(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)

        existing_project_id = repo.projects[0].id

        updated_project = usecase(
            project_id=existing_project_id,
            new_title="Dev bank",
            new_description="Projeto do processo seletivo para Dev Community"
        )

        assert updated_project.title == "Dev bank"
        assert updated_project.description == "Projeto do processo seletivo para Dev Community"

    def test_update_project_usecase_with_associates_and_display_image(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)

        existing_project_id = repo.projects[0].id
        new_associates = [uuid.uuid4(), uuid.uuid4()]

        updated_project = usecase(
            project_id=existing_project_id,
            new_title="Dev bank",
            new_description="Projeto do processo seletivo para Dev Community",
            new_associates=new_associates,
            new_display_image="https://exemplo.com/nova-imagem.png"
        )

        assert updated_project.associates == new_associates
        assert updated_project.display_image == "https://exemplo.com/nova-imagem.png"

    def test_update_project_usecase_not_found(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(
                project_id=uuid.uuid4(),
                new_title="Dev bank",
                new_description="Projeto do processo seletivo para Dev Community"
            )

    def test_update_project_usecase_wrong_project_id_type(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(
                project_id="invalid",
                new_title="Dev bank",
                new_description="Projeto do processo seletivo para Dev Community"
            )

    def test_update_project_usecase_wrong_new_title(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)

        existing_project_id = repo.projects[0].id

        with pytest.raises(EntityError):
            usecase(
                project_id=existing_project_id,
                new_title=1,
                new_description="Projeto do processo seletivo para Dev Community"
            )

    def test_update_project_usecase_wrong_new_description(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)

        existing_project_id = repo.projects[0].id

        with pytest.raises(EntityError):
            usecase(
                project_id=existing_project_id,
                new_title="Dev bank",
                new_description=1
            )

    def test_update_project_usecase_wrong_new_associates_type(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)

        existing_project_id = repo.projects[0].id

        with pytest.raises(EntityError):
            usecase(
                project_id=existing_project_id,
                new_title="Dev bank",
                new_description="Projeto do processo seletivo para Dev Community",
                new_associates="não é uma lista"
            )

    def test_update_project_usecase_wrong_new_display_image_type(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)

        existing_project_id = repo.projects[0].id

        with pytest.raises(EntityError):
            usecase(
                project_id=existing_project_id,
                new_title="Dev bank",
                new_description="Projeto do processo seletivo para Dev Community",
                new_display_image=123
            )

