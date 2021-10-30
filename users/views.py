from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ParseError


# Create your views here.
class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):
    '''Blacklist refresh token and log out'''

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(data={'detail': "User logged out successfully"}, status=status.HTTP_200_OK)

        except KeyError:
            raise ParseError(
                data={"detail": "Provide a refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
