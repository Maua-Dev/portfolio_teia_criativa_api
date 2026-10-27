from src.modules.user.create_user.app.create_user_controller import CreateUserController
from src.modules.user.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def make_admin(repo: UserRepositoryMock):
    repo.users[0] = repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
    return repo.users[0]


class Test_CreateUserController:
    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        admin = make_admin(repo)
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'teste_controller@teste.com',
            'user_name': 'user_name_test1',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(admin.id)},
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['email'] == 'teste_controller@teste.com'
        assert response.body['role'] == 'User'
        assert response.body['active'] == True
        assert response.body['user_name'] == 'user_name_test1'
        assert response.body['message'] == "the user was created successfully"

    def test_create_user_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'user_name': 'user_name_test1'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_create_user_controller_missing_user_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'teste_controller@teste.com'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_name is missing"

    def test_create_user_controller_wrong_type_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 12345
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "email" in response.body

    def test_create_user_controller_wrong_type_user_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'teste_controller@teste.com',
            'user_name': 12345
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "user_name" in response.body

    def test_create_user_controller_missing_authorizer_user(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'teste_controller@teste.com',
            'user_name': 'user_name_test1',
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == f"Field {USER_FROM_AUTHORIZER_KEY} is missing"

    def test_create_user_controller_forbidden_for_non_admin(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'teste_controller@teste.com',
            'user_name': 'user_name_test1',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(repo.users[0].id)},
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    def test_create_user_controller_forbidden_for_inactive_admin(self):
        repo = UserRepositoryMock()
        repo.users[0] = repo.users[0].model_copy(
            update={"role": RoleEnum.ADMIN, "active": False}
        )
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'teste_controller@teste.com',
            'user_name': 'user_name_test1',
            USER_FROM_AUTHORIZER_KEY: {"sub": str(repo.users[0].id)},
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "That action is forbidden for this user"

    #def test_create_user_controller_invalid_email(self):
        #repo = UserRepositoryMock()
        #usecase = CreateUserUsecase(repo=repo)
        #controller = CreateUserController(usecase=usecase)

        #request = HttpRequest(body={
            #'name': 'Branco do Branco Branco da Silva',
            #'email': 'branco@branco'})

        #response = controller(request=request)

        #assert response.status_code == 400
        #assert response.body == "Field email is not valid"

    #def test_create_user_controller_invalid_name(self):
        #repo = UserRepositoryMock()
        #usecase = CreateUserUsecase(repo=repo)
        #controller = CreateUserController(usecase=usecase)

        #request = HttpRequest(body={
            #'name': 'B',
            #'email': 'branco@branco.com'})

       #response = controller(request=request)

        #assert response.status_code == 400
        #assert response.body == "Field name is not valid"





