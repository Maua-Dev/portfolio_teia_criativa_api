from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserControler:
    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'teste_controller@teste.com',
            'senha_hash': 'senha_hash_controller'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['email'] == 'teste_controller@teste.com'
        assert response.body['role'] == 'User'
        assert response.body['message'] == "the user was created successfully"

    def test_create_user_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'senha_hash': 'senha_hash_controller'})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_create_user_controller_missing_senha_hash(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(body={
            'email': 'teste_controller@teste.com'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field senha_hash is missing"

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





