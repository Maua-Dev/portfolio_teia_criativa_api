from urllib.parse import urlparse

from src.modules.member.update_member.app.update_member_usecase import UpdateMemberUsecase
from src.modules.member.update_member.app.update_member_viewmodel import UpdateMemberViewModel
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.errors.controller_errors import (
    InvalidImageUrl,
    MissingParameters,
    WrongTypeParameter,
)
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    Forbidden,
    InternalServerError,
    NotFound,
    OK,
)


class UpdateMemberController:
    def __init__(self, usecase: UpdateMemberUsecase):
        self.UpdateMemberUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            member_id = self._required_string(request, "member_id")
            member_photo = self._required_string(request, "new_member_photo")
            member_name = self._required_string(request, "new_member_name")
            member_intro = self._required_string(request, "new_member_intro")

            parsed_url = urlparse(member_photo)
            if (
                parsed_url.scheme not in ("http", "https")
                or not parsed_url.netloc
                or not parsed_url.path.lower().endswith(
                    (".jpg", ".jpeg", ".png", ".webp")
                )
            ):
                raise InvalidImageUrl(
                    "new_member_photo must be a valid URL pointing to a JPG, JPEG, PNG or WEBP image"
                )

            member = self.UpdateMemberUsecase(
                member_id=member_id,
                member_photo=member_photo,
                member_name=member_name,
                member_intro=member_intro,
                requester_id=self._get_requester_id(request),
            )
            return OK(UpdateMemberViewModel(member).to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)
        except ForbiddenAction as err:
            return Forbidden(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except InvalidImageUrl as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=err)

    @staticmethod
    def _required_string(request: IRequest, field: str) -> str:
        value = request.data.get(field)
        if value is None:
            raise MissingParameters(field)
        if not isinstance(value, str):
            raise WrongTypeParameter(
                fieldName=field,
                fieldTypeExpected="str",
                fieldTypeReceived=type(value).__name__,
            )
        return value

    @staticmethod
    def _get_requester_id(request: IRequest) -> str | None:
        authorizer_user = request.data.get(USER_FROM_AUTHORIZER_KEY)
        if not isinstance(authorizer_user, dict):
            return None

        sub = authorizer_user.get("sub")
        return sub if isinstance(sub, str) else None
