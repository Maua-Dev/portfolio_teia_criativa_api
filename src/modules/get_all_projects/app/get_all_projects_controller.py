from typing import List

from src.shared.helpers.external_interfaces.external_interface import IRequest
from .get_all_projects_usecase import GetAllProjectsUsecase
from .get_all_projects_viewmodel import GetAllProjectsViewmodel
from src.shared.domain.entities.project import Project
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import NotFound, OK, BadRequest, InternalServerError


class GetAllProjectsController:
    def __init__(self, usecase: GetAllProjectsUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest):
        try:
            all_projects_list: List[Project] = self.usecase()

            viewmodel = GetAllProjectsViewmodel(all_projects_list)

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
