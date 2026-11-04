from src.modules.get_all_members.app.get_all_members_controller import GetAllMembersController
from src.modules.get_all_members.app.get_all_members_usecase import GetAllMembersUsecase
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestGetAllMembersController:
    def test_returns_ok_response(self):
        controller = GetAllMembersController(GetAllMembersUsecase(MemberRepositoryMock()))

        response = controller(None)

        assert response.status_code == 200
        assert response.body["all_members"]
