from src.modules.project.create_project.app.create_project_controller import CreateProjectController
from src.modules.project.create_project.app.create_project_usecase import CreateProjectUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def make_admin(repo: UserRepositoryMock):
    repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
    return repo.users[0]


class Test_CreateProjectController:
    def test_create_project_controller(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        admin = make_admin(user_repo)
        usecase = CreateProjectUsecase(repo=repo, user_repo=user_repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Novo projeto',
            'description': 'Projeto criado no teste',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(admin.id)},
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['title'] == repo.projects[-1].title
        assert response.body['description'] == repo.projects[-1].description
        assert response.body['message'] == "the project was created successfully"

    def test_create_project_controller_missing_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo, user_repo=UserRepositoryMock())
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'description': 'Projeto criado no teste'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field title is missing"

    def test_create_project_controller_missing_description(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo, user_repo=UserRepositoryMock())
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Novo projeto'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field description is missing"

    def test_create_project_controller_wrong_type_title(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo, user_repo=UserRepositoryMock())
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 123,
            'description': 'Projeto criado no teste'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'title' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_create_project_controller_missing_authorizer_user(self):
        repo = ProjectRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo, user_repo=UserRepositoryMock())
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Novo projeto',
            'description': 'Projeto criado no teste',
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == f"Field {USER_FROM_AUTHORIZER_KEY} is missing"

    def test_create_project_controller_forbidden_for_non_admin(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = CreateProjectUsecase(repo=repo, user_repo=user_repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Novo projeto',
            'description': 'Projeto criado no teste',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(user_repo.users[0].id)},
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_create_project_controller_forbidden_for_inactive_admin(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        user_repo.users[0] = user_repo.users[0].model_copy(
            update={"role": RoleEnum.ADMIN, "active": False}
        )
        usecase = CreateProjectUsecase(repo=repo, user_repo=user_repo)
        controller = CreateProjectController(usecase=usecase)

        request = HttpRequest(body={
            'title': 'Novo projeto',
            'description': 'Projeto criado no teste',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(user_repo.users[0].id)},
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"
