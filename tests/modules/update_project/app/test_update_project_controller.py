import uuid

from src.modules.update_project.app.update_project_controller import UpdateProjectController
from src.modules.update_project.app.update_project_usecase import UpdateProjectUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_UpdateProjectController:

    def test_update_project_controller(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        existing_project_id = str(repo.projects[0].id)

        request = HttpRequest(body={
            'project_id': existing_project_id,
            'new_title': 'Dev bank',
            'new_description': 'Projeto do processo seletivo para Dev Community'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['project_id'] == existing_project_id
        assert response.body['title'] == 'Dev bank'
        assert response.body['description'] == 'Projeto do processo seletivo para Dev Community'
        assert response.body['message'] == "the project was updated successfully"

    def test_update_project_controller_missing_project_id(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'new_title': 'Dev Bank',
            'new_description': 'Projeto do processo seletivo para Dev Community'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field project_id is missing"

    def test_update_project_controller_missing_new_title(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'project_id': str(repo.projects[0].id),
            'new_description': 'Projeto do processo seletivo para Dev Community'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_title is missing"

    def test_update_project_controller_missing_new_description(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'project_id': str(repo.projects[0].id),
            'new_title': 'Dev Bank'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_description is missing"

    def test_update_project_controller_wrong_type_project_id(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'project_id': 123,
            'new_title': 'Dev Bank',
            'new_description': 'Projeto do processo seletivo para Dev Community'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field project_id isn't in the right type.\n Received: int.\n Expected: str"

    def test_update_project_controller_wrong_type_new_title(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'project_id': str(repo.projects[0].id),
            'new_title': 123,
            'new_description': 'Projeto do processo seletivo para Dev Community'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_title isn't in the right type.\n Received: int.\n Expected: str"

    def test_update_project_controller_wrong_type_new_description(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'project_id': str(repo.projects[0].id),
            'new_title': 'Dev Bank',
            'new_description': 123
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_description isn't in the right type.\n Received: int.\n Expected: str"

    def test_update_project_controller_invalid_project_id_format(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'project_id': 'não-é-um-uuid',
            'new_title': 'Dev Bank',
            'new_description': 'Projeto do processo seletivo para Dev Community'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field project_id is not valid"

    def test_update_project_controller_not_found(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'project_id': str(uuid.uuid4()),
            'new_title': 'Dev Bank',
            'new_description': 'Projeto do processo seletivo para Dev Community'
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for project_id'