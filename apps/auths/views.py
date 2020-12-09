import logging

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import views, exceptions
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import (
    LoginSerializer,
)

# A workaround to check exist user in dev env
# TODO: Need to move to core/firebase.py

logger = logging.getLogger(__name__)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login",
        request_body=LoginSerializer,
        responses={200: LoginSerializer()},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        password = serializer.validated_data.get("password")
        try:
            user = authenticate(phone=phone, password=password)
        except exceptions.NotFound:
            raise APIException(
                _("User or password is wrong"),
                status.HTTP_404_NOT_FOUND,
            )
        except:
            raise APIException(_("Invalid token"), status.HTTP_400_BAD_REQUEST)
        if not user:
            raise APIException(
                _("User with phone {phone} not found").format(phone=phone),
                status.HTTP_404_NOT_FOUND,
            )
        if not user.is_active:
            raise APIException(
                _("User with phone {phone} has been blocked").format(phone=user.phone),
                status.HTTP_403_FORBIDDEN,
            )
        token = user.token
        data = {"token": token}
        return Response(data=data, status=status.HTTP_200_OK)
