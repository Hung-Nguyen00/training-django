from django.contrib.auth.models import Group, Permission
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import PasswordChangeSerializer, PasswordResetSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from usermodel.models import  User
from usermodel.validators import EmailValidator, PasswordValidator
from user_auth.services import get_user


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField("get_user_role")

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "username",
            "email",
            "is_active",
        )
        extra_kwargs = {"password": {"write_only": True}}
        validators = [UniqueTogetherValidator(queryset=User.objects.all(), fields=["username"])]

    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        allow_null=False,
        validators=[EmailValidator(), UniqueValidator(queryset=User.objects.all(), lookup="iexact")],
    )
   
    @classmethod
    def get_avatar(cls, obj):
        return obj.get_avatar()



class UserRegisterSerializer(RegisterSerializer):
    avatar = serializers.CharField(max_length=1000, required=False, default="")
    username = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=False,
        validators=[UniqueValidator(queryset=User.objects.all(), lookup="iexact")],
    )
    email = serializers.EmailField(required=True, allow_null=False, validators=[EmailValidator()])
    first_name = serializers.CharField(max_length=30, required=False, default="")
    last_name = serializers.CharField(max_length=150, required=False, default="")
    password1 = serializers.CharField(write_only=True, validators=[PasswordValidator()])

    def custom_signup(self, request, user):
        user.avatar = self.validated_data.get("avatar", None)
        user.phone = self.validated_data.get("phone", "")
        user.display_name = self.validated_data.get("display_name", "")
        user.bio = self.validated_data.get("bio", "")
        user.save()




class UserPasswordChangeSerializer(PasswordChangeSerializer):
    old_password = serializers.CharField(max_length=128, allow_blank=True)
    new_password1 = serializers.CharField(
        max_length=128, allow_blank=True, validators=[PasswordValidator(old_password)]
    )
    new_password2 = serializers.CharField(max_length=128, allow_blank=True)



class UserTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])

        # check exist user
        user_id = refresh.payload.get("id", None)
        user = get_user(user_id=user_id)

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = str(refresh)

        return data


class ResponseTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)


class UserLoginBodySerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ResendConfirmBodySerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


# class RolesSerializer(serializers.ModelSerializer):
#     role = serializers.SerializerMethodField()
#     description = serializers.SerializerMethodField()

#     class Meta:
#         model = Group
#         fields = (
#             "id",
#             "name",
#             "role",
#             "description",
#         )

#     def get_role(self, obj):
#         return retrieve_role(obj.name).role

#     def get_description(self, obj):
#         return retrieve_role(obj.name).description
