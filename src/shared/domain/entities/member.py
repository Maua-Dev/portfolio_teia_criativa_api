from pydantic import BaseModel, HttpUrl, field_validator, UUID4

class Member(BaseModel):
    member_id: UUID4
    member_photo: HttpUrl
    member_name: str
    member_intro: str

    @field_validator("member_photo")
    @classmethod
    def validate_photo_extension(cls, v: HttpUrl):
        if not str(v).lower().endswith(".jpg"):
            raise ValueError("A foto do membro deve ter a extensão .jpg")
        return v