from pydantic import HttpUrl

from src.modules.create_member.app.create_member_controller import CreateMemberController
from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestCreateMemberController:
    def test_create_member_controller(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['member_photo'] == 'https://picsum.photos/800/600.jpg'
        assert response.body['member_name'] == 'nome_membro'
        assert response.body['member_intro'] == 'intro_membro'
        assert response.body['message'] == 'the member was created succefully'

    def test_create_member_controller_missing_member_photo(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_photo is missing'

    def test_create_member_controller_missing_member_name(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_name is missing'

    def test_create_member_controller_missing_member_intro(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 'nome_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_intro is missing'

    def test_create_member_controller_wrong_type_member_photo(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_photo': 123,
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_photo' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_create_member_controller_wrong_type_member_name(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 123,
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_name' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_create_member_controller_wrong_type_member_intro(self):
        repo = MemberRepositoryMock()
        usecase = CreateMemberUsecase(repo=repo)
        controller = CreateMemberController(usecase=usecase)

        request = HttpRequest(body={
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 'nome_membro',
            'member_intro': 123
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_intro' has the wrong type. Received: 'int'. Expected: 'str'."


