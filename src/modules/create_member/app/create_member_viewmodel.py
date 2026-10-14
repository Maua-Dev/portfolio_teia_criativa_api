from pydantic import UUID4, HttpUrl

from src.shared.domain.entities.member import Member


class CreateMemberViewModel:
    member_id: str
    member_photo: str
    member_name: str
    member_intro: str

    def __init__(self, member: Member):
        self.member_id = str(member.member_id)
        self.member_photo = str(member.member_photo)
        self.member_name = member.member_name
        self.member_intro = member.member_intro

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'member_photo': self.member_photo,
            'member_name' : self.member_name,
            'member_intro' : self.member_intro,
            'message' : "the member was created succefully"
        }
        

        

    