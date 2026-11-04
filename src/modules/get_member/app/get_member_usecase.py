import uuid

from src.shared.domain.entities.member import Member
from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS


class GetMemberUsecase:
    def __init__(self, repo: IMemberRepository, observability: ObservabilityAWS):
        self.repo = repo
        self.observability = observability

    def __call__(self, member_id: str) -> Member:
        self.observability.log_usecase_in()
        if type(member_id) is not str:
            raise EntityError("member_id")

        try:
            parsed_id = uuid.UUID(member_id)
        except ValueError:
            raise EntityError("member_id")

        member = self.repo.get_member(parsed_id)
        if member is None:
            raise NoItemsFound("member_id")

        self.observability.log_usecase_out()
        return member
