from src.modules.user.update_user.app.update_user_controller import UpdateUserController
from src.modules.user.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

import uuid


def make_admin(repo: UserRepositoryMock):
    repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
    return repo.users[0]


class Test_UpdateUserController:
    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        admin = make_admin(repo)
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        existing_user_id = str(repo.users[0].id)

        request = HttpRequest(body={
            'user_id': existing_user_id,
            'new_email': 'testeemail@devmaua.com.br',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(admin.id)},
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['user_id'] == existing_user_id
        assert response.body['email'] == 'testeemail@devmaua.com.br'
        assert response.body['role'] == repo.users[0].role.value
        assert response.body['message'] == "the user was updated successfully"

    def test_update_user_controller_missing_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'new_email': 'testeemail@devmaua.com.br'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_id is missing"

    def test_update_user_controller_missing_new_email(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': str(uuid.uuid4())
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_email is missing"

    def test_update_user_controller_invalid_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': 3,
            'new_email': 'testeemail@devmaua.com.br'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'user_id' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_update_user_controller_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': str(uuid.uuid4()),
            'new_email': 'email_invalido'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'new_email' has the wrong type. Received: 'email_invalido'. Expected: 'valid email'."

    def test_update_user_not_found(self):
        repo = UserRepositoryMock()
        admin = make_admin(repo)
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': str(uuid.uuid4()),
            'new_email': 'testeemail@devmaua.com.br',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(admin.id)},
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == 'No items found for user_id'

    def test_update_user_controller_missing_authorizer_user(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': str(repo.users[0].id),
            'new_email': 'testeemail@devmaua.com.br',
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == f"Field {USER_FROM_AUTHORIZER_KEY} is missing"

    def test_update_user_controller_forbidden_for_non_admin(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': str(repo.users[1].id),
            'new_email': 'testeemail@devmaua.com.br',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(repo.users[0].id)},
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_update_user_controller_forbidden_for_inactive_admin(self):
        repo = UserRepositoryMock()
        repo.users[0] = repo.users[0].model_copy(
            update={"role": RoleEnum.ADMIN, "active": False}
        )
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_id': str(repo.users[1].id),
            'new_email': 'testeemail@devmaua.com.br',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(repo.users[0].id)},
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"
