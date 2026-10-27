
from src.modules.create_member.app.create_member_controller import CreateMemberController
from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.environments import Environments
from pprint import pprint

repo = Environments.get_member_repo()()
user_repo: IUserRepository = Environments.get_user_repo()()
usecase = CreateMemberUsecase(repo, user_repo)
controller = CreateMemberController(usecase)

def lambda_handler(event, context):

    pprint(event)

    httpRequest = LambdaHttpRequest(event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    
    return httpResponse.toDict()
    
    