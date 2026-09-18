from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_project_usecase import UpdateProjectUsecase
from .update_project_viewmodel import UpdateProjectViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
import uuid


class UpdateProjectController:

    def __init__(self, usecase: UpdateProjectUsecase):
        self.UpdateProjectUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('project_id') is None:
                raise MissingParameters('project_id')
            if request.data.get('new_title') is None:
                raise MissingParameters('new_title')
            if request.data.get('new_description') is None:
                raise MissingParameters('new_description')

            if type(request.data.get('project_id')) != str:
                raise WrongTypeParameter(
                    fieldName="project_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('project_id').__class__.__name__
                )

            if type(request.data.get('new_title')) != str:
                raise WrongTypeParameter(
                    fieldName="new_title",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('new_title').__class__.__name__
                )

            if type(request.data.get('new_description')) != str:
                raise WrongTypeParameter(
                    fieldName="new_description",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('new_description').__class__.__name__
                )

            try:
                project_id = uuid.UUID(request.data.get('project_id'))
            except ValueError:
                raise EntityError("project_id")

            project = self.UpdateProjectUsecase(
                project_id=project_id,
                new_title=request.data.get('new_title'),
                new_description=request.data.get('new_description')
            )

            viewmodel = UpdateProjectViewmodel(project=project)

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