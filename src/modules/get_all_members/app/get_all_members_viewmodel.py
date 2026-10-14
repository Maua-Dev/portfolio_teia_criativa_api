from typing import List

from src.shared.domain.entities.member import Member


class MemberViewmodel:
    def __init__(self, member: Member):
        self.member = member

    def to_dict(self):
        return {
            "member_id": str(self.member.member_id),
            "member_photo": str(self.member.member_photo),
            "member_name": self.member.member_name,
            "member_intro": self.member.member_intro,
        }


class GetAllMembersViewmodel:
    def __init__(self, members_list: List[Member]):
        self.members_viewmodel_list = [MemberViewmodel(member) for member in members_list]

    def to_dict(self):
        return {
            "all_members": [viewmodel.to_dict() for viewmodel in self.members_viewmodel_list],
            "message": "all members has been retrieved",
        }
