from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from supplierapi.utils.views import CustomViewSet

from .models import User
from .serializers import UserDetailSerializer, UserListSerializer, UserUpdateSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": str(user.pk),
            }
        )


class UserViewSet(CustomViewSet):
    """The viewset for the User model."""

    queryset = User.objects.all()

    # mapping serializer into the action
    serializer_classes = {
        "list": UserListSerializer,
        "retrieve": UserDetailSerializer,
        "update": UserUpdateSerializer,
        "create": UserDetailSerializer,
    }
    default_serializer_class = UserListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
