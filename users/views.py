from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response

from .serializers import *
from .models import Profile

# Create your views here.


# 회원 가입 api
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# 로그인 api
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data   # validate() 의 Token 을 받아 옴.
        return Response({"token": token.key})


# 프로필 api
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
