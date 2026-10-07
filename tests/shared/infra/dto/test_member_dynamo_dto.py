import uuid
from pydantic import HttpUrl

from src.shared.domain.entities.member import Member
from src.shared.infra.dto.member_dynamo_dto import MemberDynamoDTO
from src.shared.infra.external.dynamo.dynamo_keys import EntityKind, PK_ATTR, SK_ATTR


class Test_MemberDynamoDTO:
    def _make_member(self) -> Member:
        return Member(
            member_id=uuid.uuid4(),
            member_photo=HttpUrl("https://teiacriativa.com/assets/teste.jpg"),
            member_name="Membro Teste",
            member_intro="Desenvolvedor de teste",
        )

    def test_from_entity_to_dynamo(self):
        member = self._make_member()

        dynamo_dict = MemberDynamoDTO.from_entity_to_dynamo(member)

        assert dynamo_dict[PK_ATTR] == EntityKind.MEMBER.value
        assert dynamo_dict[SK_ATTR] == f"MEMBER#{member.member_id}"
        assert dynamo_dict["member_id"] == str(member.member_id)
        assert dynamo_dict["member_photo"] == str(member.member_photo)
        assert dynamo_dict["member_name"] == member.member_name
        assert dynamo_dict["member_intro"] == member.member_intro

    def test_from_entity_to_dynamo_values_are_strings(self):
        member = self._make_member()

        dynamo_dict = MemberDynamoDTO.from_entity_to_dynamo(member)

        assert isinstance(dynamo_dict["member_id"], str)
        assert isinstance(dynamo_dict["member_photo"], str)

    def test_from_dynamo_to_entity_roundtrip(self):
        member = self._make_member()

        dynamo_dict = MemberDynamoDTO.from_entity_to_dynamo(member)
        entity = MemberDynamoDTO.from_dynamo_to_entity(dynamo_dict)

        assert entity.member_id == member.member_id
        assert entity.member_photo == member.member_photo
        assert entity.member_name == member.member_name
        assert entity.member_intro == member.member_intro