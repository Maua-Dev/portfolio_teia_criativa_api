from src.shared.domain.entities.member import Member


class DeleteMemberViewmodel:
    def __init__(self, member: Member):
        self.member = member

    def to_dict(self) -> dict:
        return {
            "member_id": str(self.member.member_id),
            "member_photo": str(self.member.member_photo),
            "member_name": self.member.member_name,
            "member_intro": self.member.member_intro,
            "message": "the member was deleted successfully",
        }
