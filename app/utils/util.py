import secrets
import string
from django.contrib.auth.hashers import make_password
from typing import Any, List, Dict 
from django.db.models.query import QuerySet
from rest_framework import serializers
from api.commons.exceptions import (
    ValidationException,
    Unauthorized,
    NotFoundException,
)
from django.core.mail.message import EmailMessage
from models_v1.models import Admin, MailTemp
from django.core.paginator import Paginator
from api.commons.constants.pagination import Pagination


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
    email = EmailMessage(subject, body, "Powake <no-reply@powake.dev>", to)
    email.content_subtype = "html"
    return email.send()


def send_email_test(subject: str, body: str, to: List[str]):
    # mail = mt.Mail(
    #     sender=mt.Address(email="mailtrap@demomailtrap.com", name="DOD"),
    #     to=[mt.Address(email=to[0])],
    #     subject=subject,
    #     html=body,
    #     category="DOD Admin",
    # )

    # client = mt.MailtrapClient(token="78e64ff24ee5cc7d21d4ee0d1d382abd")
    # client.send(mail)
    from django.core.mail import EmailMultiAlternatives

    subject = subject
    text_content = "This is the plain text version."
    html_content = body
    from_email = "tranlequybaotk12@gmail.com"
    to = to

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def pagination_items(
    items: QuerySet,
    serializer: serializers,
    current_page: Any,
    per_page: Any,
    context: dict = None,
    all: str = None,
) -> Dict:
    """
    Function get pagination of list queryset with current_page and per_page
    Input
    ----------
        items: QuerySet,
        serializer: serializers,
        current_page: Any,
        per_page: Any
        context: dict (context of serializers)

    Returns
    ----------
        List items of serializers
    """

    if all is None or all.strip().lower() != "true":
        print(">>>>>>>>>>")

        if current_page.isnumeric() and int(current_page) > 0:
            current_page = int(current_page)
        else:
            current_page = Pagination.CURRENT_PAGE

        if per_page.isnumeric() and int(per_page) > 0:
            per_page = int(per_page)
        else:
            per_page = Pagination.PER_PAGE

        # Convert list items to pagination
        page_items = Paginator(items, per_page)

        items = page_items.get_page(current_page)

    print(">>>>>>>>>>")

    # Convert list object items to serializers data
    data = serializer(items, many=True, context=context).data

    # Setting current_page, per_page and total response when param all = true
    if all is None or all.strip().lower() != "true":
        current_page = (
            page_items.num_pages
            if page_items.num_pages < current_page
            else current_page
        )
        total = page_items.count
    else:
        current_page = Pagination.CURRENT_PAGE
        per_page = total = len(data)

    # Format data response of pagination list
    result = {
        "current_page": current_page,
        "per_page": per_page,
        "total": total,
        "items": data,
    }

    return result