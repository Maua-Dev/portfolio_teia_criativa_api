import uuid
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .get_project_usecase import GetProjectUsecase
from .get_project_viewmodel import GetProjectViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError



class GetProjectController:

    def __init__(self, usecase: GetProjectUsecase, observability: ObservabilityAWS):
        self.GetProjectUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            if request.data.get('project_id') is None:
                raise MissingParameters('project_id')

            if type(request.data.get('project_id')) != str:
                raise WrongTypeParameter(
                    fieldName="project_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('project_id').__class__.__name__
                )

            try:
                project_id = uuid.UUID(request.data.get('project_id'))
            except ValueError:
                raise EntityError("project_id")

            project = self.GetProjectUsecase(
                project_id=project_id
            )

            viewmodel = GetProjectViewmodel(project)
            
            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=project.id)
            return response

        except NoItemsFound as err:
            self.observability.log_exception(message=err.message)
            return NotFound(body=err.message)

        except MissingParameters as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EntityError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(message=err.args[0])
            return InternalServerError(body=err.args[0])