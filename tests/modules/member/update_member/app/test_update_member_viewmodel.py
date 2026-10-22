from src.modules.member.update_member.app.update_member_viewmodel import UpdateMemberViewmodel
from src.shared.domain.entities.member import Member


class TestUpdateMemberViewmodel:
    def test_update_member_viewmodel(self):
        member = Member(
            member_id="f4019bd7-52d3-463d-8ab1-1d373c004a43",
            member_photo="https://teiacriativa.com/assets/alice.jpg",
            member_name="Alice Silva",
            member_intro="Desenvolvedora Backend",
        )

        updated_member_viewmodel = UpdateMemberViewmodel(member)

        expected = {
            "member_id": "f4019bd7-52d3-463d-8ab1-1d373c004a43",
            "member_photo": "https://teiacriativa.com/assets/alice.jpg",
            "member_name": "Alice Silva",
            "member_intro": "Desenvolvedora Backend",
            "message": "the member was updated successfully",
        }

        assert expected == updated_member_viewmodel.to_dict()
