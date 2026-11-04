from src.modules.member.update_member.app.update_member_viewmodel import UpdateMemberViewModel
from src.shared.domain.entities.member import Member


def test_update_member_viewmodel():
    member = Member(
        member_id="f4019bd7-52d3-463d-8ab1-1d373c004a43",
        member_photo="https://picsum.photos/800/600.jpg",
        member_name="updated_name",
        member_intro="updated_intro",
    )

    viewmodel = UpdateMemberViewModel(member)

    assert viewmodel.to_dict() == {
        "member_id": str(member.member_id),
        "member_photo": str(member.member_photo),
        "member_name": "updated_name",
        "member_intro": "updated_intro",
        "message": "the member was updated successfully",
    }
