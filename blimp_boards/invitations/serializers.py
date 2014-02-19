from rest_framework import serializers

from ..accounts.models import Account
from .models import SignupRequest


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupRequest
        fields = ('email',)


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
        user_data = {
            'email': attrs['email'],
            'created_by': self.account.owner.user
        }

        self.account.invite_user(user_data)

        return attrs