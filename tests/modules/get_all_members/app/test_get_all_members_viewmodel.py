from src.modules.get_all_members.app.get_all_members_viewmodel import (
    GetAllMembersViewmodel,
    MemberViewmodel,
)
from src.shared.infra.repositories.member_repository_mock import MemberRepositoryMock


class TestGetAllMembersViewmodel:
    def test_serializes_all_members(self):
        members = MemberRepositoryMock().get_all_members()

        response = GetAllMembersViewmodel(members).to_dict()

        assert response == {
            "all_members": [
                {
                    "member_id": str(member.member_id),
                    "member_photo": str(member.member_photo),
                    "member_name": member.member_name,
                    "member_intro": member.member_intro,
                }
                for member in members
            ],
            "message": "all members has been retrieved",
        }

    def test_member_viewmodel_serializes_url_and_uuid(self):
        member = MemberRepositoryMock().get_all_members()[0]

        response = MemberViewmodel(member).to_dict()

        assert response == {
            "member_id": str(member.member_id),
            "member_photo": str(member.member_photo),
            "member_name": member.member_name,
            "member_intro": member.member_intro,
        }
