from .get_all_projects_controller import GetAllProjectsController
from .get_all_projects_usecase import GetAllProjectsUsecase
from src.shared.domain.repositories.project_repository_interface import IProjectRepository
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo: IProjectRepository = Environments.get_project_repo()()
usecase = GetAllProjectsUsecase(repo)
controller = GetAllProjectsController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()