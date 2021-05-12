from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
            }
        )


class UserViewSet(ModelViewSet):
    """The viewset for the User model."""

    queryset = User.objects.all()

    # mapping serializer into the action
    serializer_classes = {
        "list": UserListSerializer,
        "retrieve": UserDetailSerializer,
        "create": UserDetailSerializer,
        "update": UserUpdateSerializer,
        "change_password": ChangePasswordSerializer,
    }
    default_serializer_class = UserListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(detail=True, methods=["POST"])
    def change_password(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            # check old password
            if not instance.check_password(
                serializer.validated_data.get("old_password")
            ):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set new password
            instance.set_password(serializer.validated_data.get("new_password"))
            instance.save()
            return Response(
                {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Password updated successfully",
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
