from rest_framework import serializers

from ..accounts.models import Account
from ..accounts.serializers import AccountSerializer
from ..boards.serializers import BoardCollaboratorSimpleSerializer
from ..users.serializers import UserSimpleSerializer
from .models import SignupRequest, InvitedUser


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupRequest
        fields = ('email',)

    def full_clean(self, instance):
        """
        Prevent error because of unique email
        before trying to get or save object.
        """
        return instance

    def save_object(self, obj, **kwargs):
        SignupRequest.objects.get_or_create(email=obj.email)


class InvitedUserSimpleSerializer(serializers.ModelSerializer):
    gravatar_url = serializers.Field(source='gravatar_url')
    username = serializers.Field(source='username')

    class Meta:
        model = InvitedUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email',
                  'gravatar_url', 'date_created', 'date_modified')


class InvitedUserFullSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    created_by = UserSimpleSerializer()
    user = UserSimpleSerializer()
    board_collaborator = BoardCollaboratorSimpleSerializer()
    signup_request_token = serializers.SerializerMethodField('get_token')

    class Meta:
        model = InvitedUser

    def get_token(self, obj):
        try:
            return SignupRequest.objects.get(email=obj.email).token
        except SignupRequest.DoesNotExist:
            pass


class InvitedUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    account = serializers.IntegerField()

    def validate_account(self, attrs, source):
        account_id = attrs[source]
        email = attrs.get('email')

        if not email:
            return attrs

        signup_domain = email.split('@')[1]

        try:
            self.account = Account.objects.get(
                pk=account_id,
                allow_signup=True,
                email_domains__domain_name=signup_domain
            )
        except Account.DoesNotExist:
            msg = 'Account does not allow signup with email address.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate(self, attrs):
        self.user_data = {
            'email': attrs['email'],
            'created_by': self.account.owner.user
        }

        return attrs

    def send_invite(self):
        self.account.invite_user(self.user_data)
