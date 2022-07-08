from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from accounts.serializers import UserSerializer, ActivateOrDeactivateAccountSerializer
from accounts.permissions import CustomIsTheAccountUser, CustomIsSuperuser
from accounts.serializers import LoginSerializer
from accounts.models import User

class UserView(ListCreateAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(ListAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        number_of_users = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:number_of_users]


class UpdateUserView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CustomIsTheAccountUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ActivateOrDeactivateAccountView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CustomIsSuperuser]
    queryset = User.objects.all()
    serializer_class = ActivateOrDeactivateAccountSerializer

class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_instance = authenticate(
            username = serializer.validated_data['email'],
            password = serializer.validated_data['password'],
        )

        if user_instance:
            token, _ = Token.objects.get_or_create(user=user_instance)
            return Response({"token": token.key})

        return Response(
            {"detail": "Invalid email or password"}, status.HTTP_401_UNAUTHORIZED
        )

        
        
