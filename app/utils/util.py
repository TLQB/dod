import secrets
import string
from django.contrib.auth.hashers import make_password
from typing import Any
from api.commons.exceptions import (
    ValidationException,
    Unauthorized,
    NotFoundException,
)
from django.core.mail.message import EmailMessage
from typing import List
import mailtrap as mt
from models_v1.models import Admin, MailTemp


def gen_password(password: str) -> str:
    """Function genaration password

    Args:
        table (str): table name ("admins" or "users") which generate password for it

    Returns:
        str: a string of password valid
    """
    return make_password(password)


def gen_hash_email() -> str:
    """Function gen hash for email when create acount

    Returns:
        str: a string of hash
    """
    hash = ""
    alphabet = string.ascii_letters + string.digits
    mail_temp_hash = list(MailTemp.objects.all().values_list("hash", flat=True))

    # Genarate hash and not exist in mail_temps table
    while True:
        hash = "".join(secrets.choice(alphabet) for i in range(15))
        if hash not in mail_temp_hash:
            break

    return hash


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


def send_email(subject: str, body: str, to: List[str]) -> int:
    """Function send email

    Args:
        subject (str): subject of email
        body (str): content of email
        to (List[str]): list of recipients email

    Returns:
        int: 1 if send success, 0 if there's nobody to send to (no recipients)
    """
    email = EmailMessage(subject=subject, body=body, to=to)
    email.content_subtype = "html"
    return email.send()


def send_email_test(subject: str, body: str, to: List[str]):
    mail = mt.Mail(
        sender=mt.Address(email="mailtrap@demomailtrap.com", name="DOD"),
        to=[mt.Address(email=to[0])],
        subject=subject,
        html=body,
        category="DOD Admin",
    )

    client = mt.MailtrapClient(token="78e64ff24ee5cc7d21d4ee0d1d382abd")
    client.send(mail)
