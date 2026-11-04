from src.shared.domain.repositories.member_repository_interface import IMemberRepository
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

from .get_all_members_controller import GetAllMembersController
from .get_all_members_usecase import GetAllMembersUsecase

repo: IMemberRepository = Environments.get_member_repo()()
usecase = GetAllMembersUsecase(repo)
controller = GetAllMembersController(usecase)


def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers,
    )
    return http_response.toDict()
