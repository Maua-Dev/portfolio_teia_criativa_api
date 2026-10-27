from src.modules.create_member.app.create_member_controller import CreateMemberController
from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestCreateMemberController:
    @staticmethod
    def _create_controller():
        repo = MemberRepositoryMock()
        user_repo = UserRepositoryMock()
        user_repo.users[0] = user_repo.users[0].model_copy(update={"role": RoleEnum.ADMIN})
        usecase = CreateMemberUsecase(repo=repo, user_repo=user_repo)
        return CreateMemberController(usecase=usecase)

    @staticmethod
    def _request(body, requester_id="af852f40-0135-406d-b5d7-7ed5dce9bc8e"):
        request = HttpRequest(body=body)
        request.data[USER_FROM_AUTHORIZER_KEY] = {"sub": requester_id}
        return request

    def test_create_member_controller(self):
        controller = self._create_controller()

        request = self._request({
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['member_photo'] == 'https://picsum.photos/800/600.jpg'
        assert response.body['member_name'] == 'nome_membro'
        assert response.body['member_intro'] == 'intro_membro'
        assert response.body['message'] == 'the member was created successfully'

    def test_create_member_controller_missing_member_photo(self):
        controller = self._create_controller()

        request = self._request({
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_photo is missing'

    def test_create_member_controller_with_wrong_photo_url(self):
        controller = self._create_controller()

        request = self._request({
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro',
            'member_photo': 'https://example.com/image.bmp'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "member_photo must be a valid URL pointing to a JPG, JPEG, PNG or WEBP image"

    def test_create_member_controller_missing_member_name(self):
        controller = self._create_controller()

        request = self._request({
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_name is missing'

    def test_create_member_controller_missing_member_intro(self):
        controller = self._create_controller()

        request = self._request({
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 'nome_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field member_intro is missing'

    def test_create_member_controller_wrong_type_member_photo(self):
        controller = self._create_controller()

        request = self._request({
            'member_photo': 123,
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_photo' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_create_member_controller_wrong_type_member_name(self):
        controller = self._create_controller()

        request = self._request({
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 123,
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_name' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_create_member_controller_wrong_type_member_intro(self):
        controller = self._create_controller()

        request = self._request({
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 'nome_membro',
            'member_intro': 123
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "The field 'member_intro' has the wrong type. Received: 'int'. Expected: 'str'."

    def test_create_member_controller_without_authenticated_user(self):
        controller = self._create_controller()
        request = HttpRequest(body={
            'member_photo': 'https://picsum.photos/800/600.jpg',
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro'
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Field requester_id is not valid'
