from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, serializers, status, validators
from rest_framework.response import Response

from ..serializers import DefaultRegisterUserSerializer


class RegisterUserSerializer(DefaultRegisterUserSerializer):
    email = serializers.EmailField(label='Email address', max_length=255,
                                   validators=[validators.UniqueValidator(queryset=get_user_model().objects.all(),
                                                                          message="Email already exists")])

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    response_fields = ['email', ]

    def get_serializer_class(self):
        serializer_class = RegisterUserSerializer
        return serializer_class

    def perform_create(self, serializer):
        kwargs = {}
        serializer.save(**kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = {
            'email': serializer.validated_data['email']
        }

        return Response(data, status=status.HTTP_201_CREATED)


register = RegisterView.as_view()
