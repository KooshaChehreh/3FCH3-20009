from django.shortcuts import render
from rest_framework.decorators import (
    api_view,
    authentication_classes,
)
from users.serializer import UsersSerializer, LoginSerializer
from exceptions import *
from jwt_auth import generate_access_token
from rest_framework.response import Response
from rest_framework import status
from users.models import User

        
@api_view(["POST"])
@authentication_classes([])
def create_user(request):
    serializer = UsersSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    if User.objects.filter(username=username).exists():
        raise UsernameAlreadyExists
    
    created_user = serializer.save()
    return Response(UsersSerializer(created_user).data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@authentication_classes([])
def login_verify_password(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]
    try:
        target_user: User = User.objects.get(username=username)
        if target_user.is_suspended():
            raise AccountSuspended
        if not target_user.check_password(entered_password=password):
            raise InvalidUsernameOrPassword
        access_token = generate_access_token(target_user)
        response_data = {
            "access_token": access_token,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        raise InvalidUsernameOrPassword
    





