from rest_framework.views import exception_handler as base_exception_handler
from rest_framework.response import Response
from api.commons.constants.api_error_code import APIErrorCode
from rest_framework.exceptions import (
    APIException,
    NotAuthenticated,
    AuthenticationFailed,
    PermissionDenied,
    ValidationError,
)
from rest_framework import status
import traceback
import sys


def _get_response(code, data=None):
    if isinstance(data, dict):
        return {"errors": [{"code": code, **data}]}
    if isinstance(data, list):
        return {"errors": [{"code": code, **item} for item in data]}

    return {"errors": [{"code": code}]}


def exception_handler(exception, context):
    response = base_exception_handler(exception, context)

    # Any unhandled exceptions will return 500
    if not response:
        tb = traceback.format_exc()
        return Response(
            data=_get_response(APIErrorCode.HTTP_500_INTERNAL_SERVER_ERROR),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Change response data of built-in unauthorized exception
    if isinstance(exception, (NotAuthenticated, AuthenticationFailed)):
        response.data = _get_response(APIErrorCode.HTTP_401_UNAUTHORIZED)

    # Change response data of built-in forbidden exception
    elif isinstance(exception, PermissionDenied):
        response.data = _get_response(APIErrorCode.HTTP_403_FORBIDDEN)

    # Change response data and status_code of ValidationError exception, raised when calling serializer.is_valid
    elif isinstance(exception, ValidationError):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.data = _get_response(
            APIErrorCode.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Change response data of APIException
    elif isinstance(exception, APIException):
        exception_detail = getattr(exception, "data", exception.detail)
        response.data = _get_response(exception.default_code, exception_detail)

    return response
