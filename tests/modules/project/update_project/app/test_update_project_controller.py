import uuid

from src.modules.project.update_project.app.update_project_controller import UpdateProjectController
from src.modules.project.update_project.app.update_project_usecase import UpdateProjectUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.project_repository_mock import ProjectRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def make_admin(repo: UserRepositoryMock):
    repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
    return repo.users[0]


class Test_UpdateProjectController:
    def test_update_project_controller(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        admin = make_admin(user_repo)
        usecase = UpdateProjectUsecase(repo=repo, user_repo=user_repo)
        controller = UpdateProjectController(usecase=usecase)
        project = repo.projects[0]

        request = HttpRequest(body={
            "project_id": str(project.id),
            "new_title": "Projeto atualizado",
            "new_description": "Descrição atualizada",
            USER_FROM_AUTHORIZER_KEY: {"sub": str(admin.id)},
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["project_id"] == str(project.id)
        assert response.body["title"] == "Projeto atualizado"
        assert response.body["description"] == "Descrição atualizada"

    def test_update_project_controller_missing_authorizer_user(self):
        repo = ProjectRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo, user_repo=UserRepositoryMock())
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "project_id": str(repo.projects[0].id),
            "new_title": "Projeto atualizado",
            "new_description": "Descrição atualizada",
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == f"Field {USER_FROM_AUTHORIZER_KEY} is missing"

    def test_update_project_controller_forbidden_for_non_admin(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = UpdateProjectUsecase(repo=repo, user_repo=user_repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "project_id": str(repo.projects[0].id),
            "new_title": "Projeto atualizado",
            "new_description": "Descrição atualizada",
            USER_FROM_AUTHORIZER_KEY: {"sub": str(user_repo.users[0].id)},
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_update_project_controller_forbidden_for_inactive_admin(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        user_repo.users[0] = user_repo.users[0].model_copy(
            update={"role": RoleEnum.ADMIN, "active": False}
        )
        usecase = UpdateProjectUsecase(repo=repo, user_repo=user_repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "project_id": str(repo.projects[0].id),
            "new_title": "Projeto atualizado",
            "new_description": "Descrição atualizada",
            USER_FROM_AUTHORIZER_KEY: {"sub": str(user_repo.users[0].id)},
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_update_project_controller_project_not_found(self):
        repo = ProjectRepositoryMock()
        user_repo = UserRepositoryMock()
        admin = make_admin(user_repo)
        usecase = UpdateProjectUsecase(repo=repo, user_repo=user_repo)
        controller = UpdateProjectController(usecase=usecase)

        request = HttpRequest(body={
            "project_id": str(uuid.uuid4()),
            "new_title": "Projeto atualizado",
            "new_description": "Descrição atualizada",
            USER_FROM_AUTHORIZER_KEY: {"sub": str(admin.id)},
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for project_id"
