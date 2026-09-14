from .get_project_controller import GetProjectController
from .get_project_usecase import GetProjectUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from aws_lambda_powertools import Logger, Tracer, Metrics


observability = Environments.get_observability()(module_name="get_project")

repo = Environments.get_project_repo()()
usecase = GetProjectUsecase(repo, observability=observability)
controller = GetProjectController(usecase, observability=observability)

@observability.presenter_decorators
def get_project_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = get_project_presenter(event)
    
    observability.add_metric(name="ErrorCount", unit="Count", value=1) if response["statusCode"] != 200 else None
    
    return response
