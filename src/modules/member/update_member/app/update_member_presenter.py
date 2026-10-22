from .update_member_controller import UpdateMemberController
from .update_member_usecase import UpdateMemberUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import (
    LambdaHttpRequest,
    LambdaHttpResponse,
)

repo = Environments.get_member_repo()()
usecase = UpdateMemberUsecase(repo)
controller = UpdateMemberController(usecase)


def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers,
    )
    return http_response.toDict()
