from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.request import HttpRequest
from models_v1.models import Admin
from api.api_v1.admins.serializers import AdminSerializer
from api.commons.validation import ValidateError, UNIQUE_ERR 
from api.commons.exceptions import ValidationException

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
        admin = Admin.objects.get(pk=admin_id)
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

        admin = Admin.objects.get(pk=admin_id)
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
        admin = Admin.objects.get(pk=admin_id)
        admin.delete()
        return Response({"delete_id": admin.id})

