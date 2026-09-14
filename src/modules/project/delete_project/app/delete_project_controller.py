import uuid

from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .delete_project_usecase import DeleteProjectUsecase
from .delete_project_viewmodel import DeleteProjectViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class DeleteProjectController:

    def __init__(self, usecase: DeleteProjectUsecase):
        self.DeleteProjectUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
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

            project = self.DeleteProjectUsecase(
                project_id=project_id
            )

            viewmodel = DeleteProjectViewmodel(project=project)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])