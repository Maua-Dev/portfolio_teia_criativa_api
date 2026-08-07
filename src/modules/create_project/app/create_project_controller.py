from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_project_usecase import CreateProjectUsecase
from .create_project_viewmodel import CreateProjectViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Created


class CreateProjectController:

    def __init__(self, usecase: CreateProjectUsecase):
        self.CreateProjectUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:

            if request.data.get('title') is None:
                raise MissingParameters('title')

            if type(request.data.get('title')) != str:
                raise WrongTypeParameter('title')
            
            if request.data.get('description') is None:
                raise MissingParameters('description')

            if type(request.data.get('description')) != str:
                raise WrongTypeParameter('description')
            
            project = self.CreateProjectUsecase(
                title=request.data.get('title'),
                description=request.data.get('description')
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