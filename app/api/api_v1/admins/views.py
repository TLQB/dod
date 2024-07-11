from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.request import HttpRequest
from models_v1.models import Admin
from api.api_v1.admins.serializers import AdminSerializer
from api.commons.validation import ValidateError, UNIQUE_ERR 
from api.commons.exceptions import ValidationException, Unauthorized, NotFoundException
from django.contrib.auth.hashers import check_password
from shares.token import TokenSerializer, AdminTokenModel, get_tokens_for_admin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.util import gen_password, get_object
from django.contrib.auth.hashers import check_password, make_password

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request: HttpRequest) -> Response:
        data: dict = request.data

        name = data.get("name")
        password = data.get("password")

        if name is None or name.strip() == "" or password is None or password.strip() == "":
            raise Unauthorized

        admin = Admin.objects.filter(name=name, is_enabled=True).first()
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


class ListCreateAdminView(APIView):
    """
    API view to handle GET and POST requests for Admin objects.
    GET request returns all existing Admin objects serialized using AdminSerializer.
    POST request creates a new Admin object using the data provided in the request.
    """
    def get(self, request: HttpRequest) -> Response:
        admins = Admin.objects.all().order_by('pk')
        admin_serializer = AdminSerializer(admins, many=True)

        return Response(admin_serializer.data)

    def post(self, request: HttpRequest) -> Response:
        """
        Create a new Admin object using the data provided in the request.
        Return the serialized version of the newly created Admin object.
        """
        data: dict = request.data

        admin = Admin.objects.filter(name=data['name'], is_enabled=True).exists() 

        if admin:
            list_error = ValidateError('name', [UNIQUE_ERR])
            raise ValidationException(list_error)

        data["password"] = gen_password(data["password"])
        admin_serializer = AdminSerializer(data=data)
        if admin_serializer.is_valid(raise_exception=True):
            admin_serializer.save()

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

