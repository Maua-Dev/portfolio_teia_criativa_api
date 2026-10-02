import pytest
from pydantic import ValidationError
from src.shared.domain.entities.member import Member

class Test_Member:
    def test_member_valid_creation(self):
        member = Member(
            member_id="c823058a-3607-4229-8473-04473e3514a6",
            member_photo="https://teiacriativa.com/images/profile.jpg",
            member_name="Carlos",
            member_intro="Engenheiro de Software"
        )
        assert member.member_name == "Carlos"
        assert str(member.member_photo) == "https://teiacriativa.com/images/profile.jpg"

    def test_member_invalid_photo_extension(self):
        with pytest.raises(ValidationError) as exc_info:
            Member(
                member_id="c823058a-3607-4229-8473-04473e3514a6",
                member_photo="https://teiacriativa.com/images/profile.png",
                member_name="Carlos",
                member_intro="Engenheiro de Software"
            )
        assert "extensão .jpg" in str(exc_info.value)

    def test_member_invalid_uuid(self):
        with pytest.raises(ValidationError):
            Member(
                member_id="id-invalido",
                member_photo="https://teiacriativa.com/images/profile.jpg",
                member_name="Carlos",
                member_intro="Engenheiro de Software"
            )