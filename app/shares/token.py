from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, Token
from typing import Dict, List, Union
import jwt
from django.conf import settings


class TokenModel:
    "Class token model"
    refresh_token: str
    access_token: str

    def __init__(self, refresh_token=None, access_token=None):
        self.refresh_token = refresh_token
        self.access_token = access_token


class TokenSerializer(serializers.Serializer):
    "Serializer of token"
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


# Token for admin
class AdminTokenModel:
    "Class item of admin token"
    id: int
    name: str
    email: str
    is_master: bool
    # policy_groups: List[int]
    # products: List[int]

    def __init__(self, id, name, email, is_master):
        self.id = id
        self.name = name
        self.email = email
        self.is_master = is_master
        # self.policy_groups = policy_groups
        # self.products = products


def get_tokens_for_admin(admin: AdminTokenModel) -> TokenModel:
    """Function get token of admin when login success

    Args:
        admin (AdminTokenModel): An object AdminTokenModel of admin

    Returns:
        TokenModel: Include refresh_token, access_token
    """
    refresh_token = RefreshToken.for_user(admin)
    access_token = refresh_token.access_token

    # Custom access_token claims
    access_token_custom = custom_admin_token_claims(str(access_token), admin)

    # Custom refresh_token claims
    refresh_token_custom = custom_admin_refresh_token_claims(str(refresh_token), admin)

    return TokenModel(str(refresh_token_custom), str(access_token_custom))
    # return TokenModel(str(refresh_token), str(access_token_custom))


def custom_admin_token_claims(access_token: str, admin: AdminTokenModel) -> str:
    """Function custom token claims
    Args:
        access_token (str): An access_token wanted to custom token claims
        admin (AdminTokenModel): Information of admin to custom token claims

    Returns:
        str: An access_token after custom token claims
    """
    print("0000000000000000000")

    # Decode token to custom token claims
    decode_jwt = jwt.decode(
        access_token, settings.__getattr__("SECRET_KEY"), algorithms=["HS256"]
    )
    print("1111111111111")

    # Custom token claims
    decode_jwt["name"] = admin.name
    decode_jwt["email"] = admin.email
    decode_jwt["is_master"] = admin.is_master
    # decode_jwt["policy_groups"] = admin.policy_groups
    # decode_jwt["products"] = admin.products
    decode_jwt["customer_key"] = settings.__getattr__("CUSTOMER_KEY")

    print("1111111111111")

    # Encode token after custom token claims
    encoded = jwt.encode(
        decode_jwt, settings.__getattr__("SECRET_KEY"), algorithm="HS256"
    )

    return encoded

def custom_admin_refresh_token_claims(
    refresh_token: str, admin: AdminTokenModel
) -> str:
    """Function custom refresh token claims
    Args:
        refresh_token (str): An refresh_token wanted to custom token claims
        admin (AdminTokenModel): Information of admin to custom token claims

    Returns:
        str: An refresh_token after custom token claims
    """

    # Decode token to custom token claims
    decode_jwt = jwt.decode(
        refresh_token, settings.__getattr__("SECRET_KEY"), algorithms=["HS256"]
    )

    # Custom token claims
    decode_jwt["id"] = admin.id
    decode_jwt["is_master"] = admin.is_master

    # Encode token after custom token claims
    encoded = jwt.encode(
        decode_jwt, settings.__getattr__("SECRET_KEY"), algorithm="HS256"
    )

    return encoded