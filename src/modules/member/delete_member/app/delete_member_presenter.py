from .delete_member_controller import DeleteMemberController
from .delete_member_usecase import DeleteMemberUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import (
    LambdaHttpRequest,
    LambdaHttpResponse,
)

repo = Environments.get_member_repo()()
usecase = DeleteMemberUsecase(repo)
controller = DeleteMemberController(usecase)


def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers,
    )
    return http_response.toDict()
