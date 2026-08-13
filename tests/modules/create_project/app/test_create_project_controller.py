import uuid

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
            'title': 'Projeto Teia',
            'description': 'Descrição do projeto',
            'associates': [str(uuid.uuid4()), str(uuid.uuid4())],
            'display_image': 'https://exemplo.com/imagem.png'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['title'] == repo.projects[-1].title
        assert response.body['description'] == repo.projects[-1].description
        assert response.body['associates'] == repo.projects[-1].associates
        assert response.body['display_image'] == repo.projects[-1].display_image
        assert response.body['message'] == "the project was created successfully"

    def test_create_project_controller_without_optional_fields(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Projeto Teia',
            'description': 'Descrição do projeto'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['associates'] is None
        assert response.body['display_image'] is None

    def test_create_project_controller_missing_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'description': 'Descrição do projeto'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field title is missing"

    def test_create_project_controller_missing_description(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Projeto Teia'
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
            'description': 'Descrição do projeto'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field title isn't in the right type."

    def test_create_project_controller_wrong_type_description(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Projeto Teia',
            'description': 123
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field description isn't in the right type."

    def test_create_project_controller_associates_wrong_type_not_list(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Projeto Teia',
            'description': 'Descrição do projeto',
            'associates': 'não é uma lista'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field associates isn't in the right type."

    def test_create_project_controller_associates_item_wrong_type(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Projeto Teia',
            'description': 'Descrição do projeto',
            'associates': [123]
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field associates isn't in the right type."

    def test_create_project_controller_associates_invalid_uuid(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Projeto Teia',
            'description': 'Descrição do projeto',
            'associates': ['']
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field associates is not valid"

    def test_create_project_controller_display_image_wrong_type(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Projeto Teia',
            'description': 'Descrição do projeto',
            'display_image': 123
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field display_image isn't in the right type."