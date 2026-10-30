from src.modules.member.delete_member.app.delete_member_controller import DeleteMemberController
from src.modules.member.delete_member.app.delete_member_usecase import DeleteMemberUsecase
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import (LambdaHttpRequest,LambdaHttpResponse,)
from src.shared.helpers.observability.wrap_handler import observed_handler


repo = Environments.get_member_repo()()
user_repo: IUserRepository = Environments.get_user_repo()()
usecase = DeleteMemberUsecase(repo=repo, user_repo=user_repo)
controller = DeleteMemberController(usecase=usecase)


@observed_handler("delete_member")
def lambda_handler(event, context):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers,
    )
    return http_response.toDict()
