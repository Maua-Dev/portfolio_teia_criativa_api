from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_project_usecase import CreateProjectUsecase
from .create_project_viewmodel import CreateProjectViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Created
import uuid


class CreateProjectController:

    def __init__(self, usecase: CreateProjectUsecase):
        self.CreateProjectUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:

            if request.data.get('title') is None:
                raise MissingParameters('title')

            if type(request.data.get('title')) != str:
                raise WrongTypeParameter(
                    fieldName='title',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(request.data.get('title')).__name__
                )

            if request.data.get('description') is None:
                raise MissingParameters('description')

            if type(request.data.get('description')) != str:
                raise WrongTypeParameter(
                    fieldName='description',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(request.data.get('description')).__name__
                )

            if request.data.get('associates') is None:
                pass
            elif type(request.data.get('associates')) != list:
                raise WrongTypeParameter(
                    fieldName='associates',
                    fieldTypeExpected='list',
                    fieldTypeReceived=type(request.data.get('associates')).__name__
                )
            else:
                for associate_id in request.data.get('associates'):
                    if type(associate_id) != str:
                        raise WrongTypeParameter(
                            fieldName='associates',
                            fieldTypeExpected='str',
                            fieldTypeReceived=type(associate_id).__name__
                        )
                    try:
                        uuid.UUID(associate_id)
                    except ValueError:
                        raise EntityError("associates")

            if request.data.get('display_image') is None:
                pass
            elif type(request.data.get('display_image')) != str:
                raise WrongTypeParameter(
                    fieldName='display_image',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(request.data.get('display_image')).__name__
                )

            
            project = self.CreateProjectUsecase(
                title=request.data.get('title'),
                description=request.data.get('description'),
                associates=request.data.get('associates', None),
                display_image=request.data.get('display_image', None)
            )

            viewmodel = CreateProjectViewmodel(project)

            return Created(viewmodel.to_dict())
            
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