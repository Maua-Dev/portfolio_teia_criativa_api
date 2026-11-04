from uuid import UUID

from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_project_usecase import UpdateProjectUsecase
from .update_project_viewmodel import UpdateProjectViewmodel
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, Forbidden, InternalServerError


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

            try:
                project_id = UUID(request.data.get('project_id'))
            except ValueError:
                raise EntityError("project_id")

            user_from_authorizer = request.data.get(USER_FROM_AUTHORIZER_KEY)
            if user_from_authorizer is None:
                raise MissingParameters(USER_FROM_AUTHORIZER_KEY)

            requester_user_id = user_from_authorizer.get("sub")
            if requester_user_id is None:
                raise MissingParameters("sub")
            if not isinstance(requester_user_id, str):
                raise WrongTypeParameter(
                    fieldName="sub",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(requester_user_id).__name__
                )

            try:
                parsed_requester_user_id = UUID(requester_user_id)
            except ValueError:
                raise EntityError("user_id")

            project = self.UpdateProjectUsecase(
                project_id=project_id,
                new_title=request.data.get('new_title'),
                new_description=request.data.get('new_description'),
                requester_user_id=parsed_requester_user_id,
            )

            viewmodel = UpdateProjectViewmodel(project=project)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except ForbiddenAction as err:

            return Forbidden(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
