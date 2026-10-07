import uuid
from src.shared.domain.entities.member import Member
from src.shared.infra.external.dynamo.dynamo_keys import (
    EntityKind,
    partition_key,
    sort_key,
    strip_keys,
    PK_ATTR,
    SK_ATTR
)


class MemberDynamoDTO:

    @staticmethod
    def from_entity_to_dynamo(member: Member) -> dict:
        return {
            PK_ATTR: partition_key(kind=EntityKind.MEMBER),
            SK_ATTR: sort_key(id=member.member_id, kind=EntityKind.MEMBER),
            "id": str(member.member_id),
            "photo": str(member.member_photo),
            "name": member.member_name,
            "intro": member.member_intro,
        }

    @staticmethod
    def from_dynamo_to_entity(member_data: dict) -> Member:
        return Member.model_validate(obj=strip_keys(member_data))