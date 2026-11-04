from src.modules.member.update_member.app.update_member_controller import UpdateMemberController
from src.modules.member.update_member.app.update_member_usecase import UpdateMemberUsecase
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import (
    LambdaHttpRequest,
    LambdaHttpResponse,
)
from src.shared.helpers.observability.wrap_handler import observed_handler


repo = Environments.get_member_repo()()
user_repo: IUserRepository = Environments.get_user_repo()()
usecase = UpdateMemberUsecase(repo=repo, user_repo=user_repo)
controller = UpdateMemberController(usecase=usecase)


@observed_handler("update_member")
def lambda_handler(event, _context):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers,
    )
    return http_response.toDict()
