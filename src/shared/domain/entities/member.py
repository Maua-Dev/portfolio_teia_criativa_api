from pydantic import BaseModel, HttpUrl, field_validator, UUID4

ALLOWED_PHOTO_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


class Member(BaseModel):
    member_id: UUID4
    member_photo: HttpUrl
    member_name: str
    member_intro: str

    @field_validator("member_photo")
    @classmethod
    def validate_photo_extension(cls, v: HttpUrl):
        if not str(v).lower().endswith(ALLOWED_PHOTO_EXTENSIONS):
            raise ValueError(
                "A foto do membro deve ter a extensão .jpg, .jpeg, .png ou .webp"
            )
        return v