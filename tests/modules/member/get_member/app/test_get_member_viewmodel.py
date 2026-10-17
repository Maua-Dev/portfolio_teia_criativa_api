from src.modules.get_member.app.get_member_viewmodel import GetMemberViewmodel
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class Test_GetMemberViewmodel:
    def test_get_member_viewmodel(self):
        member = MemberRepositoryMock().members[0]

        assert GetMemberViewmodel(member).to_dict() == {
            "member_id": str(member.member_id),
            "member_photo": str(member.member_photo),
            "member_name": "Alice Silva",
            "member_intro": "Desenvolvedora Backend",
            "message": "the member was retrieved successfully",
        }
