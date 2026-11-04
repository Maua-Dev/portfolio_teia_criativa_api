from src.modules.get_all_members.app.get_all_members_usecase import GetAllMembersUsecase
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestGetAllMembersUsecase:
    def test_returns_members_from_repository(self):
        repo = MemberRepositoryMock()

        members = GetAllMembersUsecase(repo)()

        assert members == repo.members
        assert len(members) == len(repo.members)
