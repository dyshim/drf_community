from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import Profile


# 회원 가입
class RegisterSerializer(serializers.ModelSerializer):
    """
    - UniqueValidator : 이메일 중복 방지 검증 도구
    - validate_password : Django의 기본 패스워드 검증 도구

    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all())],   # 이메일 중복 검증
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],   # 비밀번호 중복 검증
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']

    # 비밀번호 일치 여부 확인
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."})

        return data

    def create(self, validated_data):
        """
        CREATE 요청 시,유저와 토큰을 생성.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user


# 로그인
class LoginSerializer(serializers.Serializer):
    """
    - write_only : 클라이언트 -> 서버 (역직렬화 가능). 서버 -> 클라이언트 (직렬화 불가능)
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "로그인할 수 없습니다."}
        )


# 프로필
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nickname', 'position', 'subjects', 'image']
