from rest_framework import status
from rest_framework.exceptions import APIException
from api.commons.constants.api_error_message import APIErrorMessage
from api.commons.constants.api_error_code import APIErrorCode

class ValidationException(APIException):
    """
    Class for validation exception.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = APIErrorCode.HTTP_422_VALIDATION_ERROR
    default_detail = APIErrorMessage.HTTP_422_VALIDATION_ERROR

    def __init__(self, data=None):
        if data is not None:
            self.data = data

        super().__init__(code=self.default_code)