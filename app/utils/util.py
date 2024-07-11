import secrets
import string
from django.contrib.auth.hashers import make_password
from typing import Any
from api.commons.exceptions import ValidationException, Unauthorized, NotFoundException

def gen_password(password: str) -> str:
    """Function genaration password

    Args:
        table (str): table name ("admins" or "users") which generate password for it

    Returns:
        str: a string of password valid
    """
    return make_password(password)

def get_object(model_object: Any, pk: Any, **kwargs) -> object:
    """
    Function get object
    Input value
    ----------
        model_object: table model
        pk : int

    Returns
    ----------
        Object

    Raises
    ----------
    NotFoundException
        if parameter pk is not exist.
    """

    try:
        if isinstance(pk, int):
            return model_object.objects.get(pk=pk, **kwargs)
        else:
            raise NotFoundException
    except model_object.DoesNotExist:
        raise NotFoundException
