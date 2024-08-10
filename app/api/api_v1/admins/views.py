from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.request import HttpRequest
from django.utils import timezone
from models_v1.models import Admin, MailTemp
from api.api_v1.admins.serializers import AdminSerializer
from api.commons.validation import ValidateError, UNIQUE_ERR
from api.commons.exceptions import (
    ValidationException,
    Unauthorized,
    NotFoundException,
)
from django.contrib.auth.hashers import check_password
from shares.token import TokenSerializer, AdminTokenModel, get_tokens_for_admin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.util import (
    gen_password,
    get_object,
    send_email,
    gen_hash_email,
    send_email_test,
    pagination_items,
)
from django.contrib.auth.hashers import check_password, make_password
from api.commons.constants.template_mail import ConstantTemplateMail
from django.template.loader import render_to_string
from api.commons.constants.admin import ConstantAdmin
from typing import Dict
from django.conf import settings
from datetime import timedelta
from api.commons.constants.admin import ConstantAdmin
from django.template.loader import render_to_string
import jwt
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from shares.token import custom_admin_token_claims


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request: HttpRequest) -> Response:
        data: dict = request.data

        username = data.get("username")
        password = data.get("password")

        if (
            username is None
            or username.strip() == ""
            or password is None
            or password.strip() == ""
        ):
            raise Unauthorized

        admin = Admin.objects.filter(
            name=username, is_mailauth_completed=True, is_enabled=True
        ).first()
        if admin is None:
            raise Unauthorized

        if check_password(password, admin.password):
            # Generate token
            admin_token_model = AdminTokenModel(
                admin.id,
                admin.name,
                admin.email,
                admin.is_master,
            )
            token = get_tokens_for_admin(admin_token_model)
            token_serializer = TokenSerializer(token)

            return Response(token_serializer.data)

        raise Unauthorized

class CheckLoginView(APIView):
    """Class check token login of admin

    Method post: check token of admin login
    """
    authentication_classes = []
    permission_classes = []
    def post(self, request: HttpRequest) -> Response:
        """API check token of admin login. Method POST

        Parameters
        ----------
        request (HttpRequest):
            The request from client

        Returns
        ----------
        Response
            New access token of admin login

        Raises
        ----------
        Unauthorized if refresh token is invalid or expired
        """

        data: dict = request.data




        # Check empty refresh token
        if data.get("refresh_token") is None:
            raise Unauthorized

        # Get data refresh token
        refresh = data["refresh_token"]

        # Decode refresh token if is expired token or invalid then raise Unauthorized
        try:
            # print(refresh, "22222222222", settings.__getattr__("SECRET_KEY") )
            decodeJTW = jwt.decode(
                refresh,
                settings.__getattr__("SECRET_KEY"),
                algorithms=["HS256"],
            )
        except Exception as e:
            print("000000000000000", e)
            raise Unauthorized



        # Check token is not token of admin
        if decodeJTW.get("is_master") is None:
            raise Unauthorized

        print("111111111111111111")

        # Convert refresh token for token refresh serializer
        data_refresh = {"refresh": refresh}
        serializer = TokenRefreshSerializer()

        # Get access token from refresh token
        access = serializer.validate(data_refresh)

        # Get admin info from database
        admin_info: Admin = Admin.objects.filter(id=decodeJTW["id"]).first()

        # Set model token
        model = AdminTokenModel(
            admin_info.id,
            admin_info.name,
            admin_info.email,
            admin_info.is_master,
        )

        # Get custom token claims
        access_token_custom = custom_admin_token_claims(access["access"], model)

        # Response access_token token
        return Response({"access_token": access_token_custom})

class ListCreateAdminView(APIView):
    """
    API view to handle GET and POST requests for Admin objects.
    GET request returns all existing Admin objects serialized using AdminSerializer.
    POST request creates a new Admin object using the data provided in the request.
    """
    def get(self, request: HttpRequest) -> Response:
        current_page = request.GET.get("current_page")
        per_page = request.GET.get("per_page")
        all = request.GET.get("all")
        admins = Admin.objects.all().order_by("pk")
        # admin_serializer = AdminSerializer(admins, many=True)
        data = pagination_items(
            admins, AdminSerializer, current_page, per_page, None, all
        )
        return Response(data)

        # return Response(admin_serializer.data)

    def post(self, request: HttpRequest) -> Response:
        """
        Create a new Admin object using the data provided in the request.
        Return the serialized version of the newly created Admin object.
        """
        data: dict = request.data

        admin = Admin.objects.filter(
            name=data["name"], is_enabled=True
        ).exists()

        if admin:
            list_error = ValidateError("name", [UNIQUE_ERR])
            raise ValidationException(vars(list_error))

        password = data["password"]
        data["password"] = gen_password(data["password"])

        # Get hash
        hash = gen_hash_email()
        expired = timezone.now() + timedelta(
            hours=int(settings.__getattr__("EXPIRED_MAIL"))
        )
        admin_serializer = AdminSerializer(data=data)
        if admin_serializer.is_valid(raise_exception=True):
            admin = admin_serializer.save()
            mail_temp = MailTemp(
                account_id=admin.id,
                expire_time=expired,
                hash=hash,
            )
            mail_temp.save()

            try:
                context = {
                    "url_active": ConstantTemplateMail.CREATE_ADMIN.url_active
                    + hash,  # Url active email
                    "expired_mail": ConstantTemplateMail.CREATE_ADMIN.expired_mail,
                    "password": password,
                }
                subject = ConstantTemplateMail.CREATE_ADMIN.subject
                to = [admin_serializer.data["email"]]
                body = render_to_string(
                    ConstantTemplateMail.CREATE_ADMIN.template, context
                )
                # Send mail
                send_email(subject, body, to)

            except Exception as e:
                print(e)

        return Response(admin_serializer.data)


class DetailEditDeleteAdminView(APIView):
    """
    API view for retrieving, updating and deleting admin details.

    Methods:
    get -- Retrieve admin details based on the admin ID provided.
    patch -- Update admin details based on the admin ID and data provided.
    delete -- Delete admin details based on the admin ID provided.
    """
    def get(self, request: HttpRequest, admin_id: int) -> Response:
        """
        Retrieve admin details from the database based on the provided admin ID.

        Keyword arguments:
        request -- The HTTP request object.
        admin_id -- The ID of the admin for which details are to be retrieved.

        Returns:
        A JSON response containing the serialized admin details.
        """
        admin = get_object(Admin, admin_id)
        admin_serializer = AdminSerializer(admin)

        return Response(admin_serializer.data)

    def patch(self, request: HttpRequest, admin_id: int) -> Response:
        """
        Update admin details in the database based on the provided admin ID and data.

        Keyword arguments:
        request -- The HTTP request object.
        admin_id -- The ID of the admin for which details are to be updated.
        data -- The data to update the admin details with.

        Returns:
        A JSON response containing the updated serialized admin details.
        """
        data: dict = request.data
        data["password"] = gen_password(data["password"])

        admin = get_object(Admin, admin_id)

        admin_serializer = AdminSerializer(admin, data=data, partial=True)
        if admin_serializer.is_valid(raise_exception=True):
            admin_serializer.save()
        return Response(admin_serializer.data)

    def delete(self, request: HttpRequest, admin_id: int) -> Response:
        """
        Delete admin details from the database based on the provided admin ID.

        Keyword arguments:
        request -- The HTTP request object.
        admin_id -- The ID of the admin to be deleted.

        Returns:
        A JSON response containing the ID of the deleted admin.
        """
        admin = get_object(Admin, admin_id)
        id_delete = admin.id
        admin.delete()
        return Response({"delete_id": id_delete})


class VerifyMailCreateAdminView(APIView):
    """API verify mail create account of admin.

    Method get: verify email url
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request: HttpRequest, hash: str) -> Response:
        """API verify email url. Method GET

        Parameters
        ----------
        request (HttpRequest):
            The request from client

            request data: None

        hash (str):
            Hash code to verify email

        Returns
        ----------
        Response
            a json empty when verify email url success

        """
        # Validation and get object
        item = get_object_verify_email_create_admin(hash)

        # Update is_mailauth_completed of admin
        data_edit = {"is_mailauth_completed": ConstantAdmin.EMAIL_VERIFIED}

        admin_serializer = AdminSerializer(
            item["admin_item"], data=data_edit, partial=True
        )

        if admin_serializer.is_valid(raise_exception=True):
            admin_serializer.save()

            # Delete mail_temp item
            MailTemp.objects.filter(pk=item["mail_temp_item"].id).delete()

        return Response({})


def get_object_verify_email_create_admin(hash: str) -> Dict[str, object]:
    """Function validate hash of verify email create admin

    Args:
        hash (str): hash code which need to verified

    Returns:
        Dict[str, object]: dict of mail_temp and admin

    Raises:
        NotFoundException if validate error
    """

    mail_temp_item: MailTemp = MailTemp.objects.filter(
        hash=hash,
        expire_time__gte=timezone.now(),
    ).first()

    if mail_temp_item is None:
        raise NotFoundException

    # Get admin have:
    # admin_id = account_id of mail_temps table
    # is_mailauth_completed
    admin_item: Admin = Admin.objects.filter(
        id=mail_temp_item.account_id,
        is_mailauth_completed=ConstantAdmin.EMAIL_NO_VERIFY,
    ).first()

    if admin_item is None:
        raise NotFoundException

    # Return value
    return_value = {"mail_temp_item": mail_temp_item, "admin_item": admin_item}

    return return_value
