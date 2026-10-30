from src.modules.member.delete_member.app.delete_member_viewmodel import DeleteMemberViewmodel
from src.shared.domain.entities.member import Member


class TestDeleteMemberViewmodel:
    def test_delete_member_viewmodel(self):
        member = Member(
            member_id="f4019bd7-52d3-463d-8ab1-1d373c004a43",
            member_photo="https://teiacriativa.com/assets/alice.jpg",
            member_name="Alice Silva",
            member_intro="Desenvolvedora Backend",
        )

        assert DeleteMemberViewmodel(member).to_dict() == {
            "member_id": str(member.member_id),
            "member_photo": str(member.member_photo),
            "member_name": member.member_name,
            "member_intro": member.member_intro,
            "message": "the member was deleted successfully",
        }
