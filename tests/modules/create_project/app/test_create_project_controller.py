from src.modules.create_project.app.create_project_controller import CreateProjectController
from src.modules.create_project.app.create_project_usecase import CreateProjectUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock


class Test_CreateProjectController:
    def test_create_project_controller(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Novo projeto',
            'description': 'Projeto criado no teste'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['title'] == repo.projects[-1].title
        assert response.body['description'] == repo.projects[-1].description
        assert response.body['message'] == "the project was created successfully"

    def test_create_project_controller_missing_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'description': 'Projeto criado no teste'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field title is missing"

    def test_create_project_controller_missing_description(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Novo projeto'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field description is missing"

    def test_create_project_controller_wrong_type_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 123,
            'description': 'Projeto criado no teste'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'title' has the wrong type. Received: 'int'. Expected: 'str'."
