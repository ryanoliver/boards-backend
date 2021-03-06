from ...utils.tests import BaseTestCase
from ...users.models import User
from ...invitations.models import InvitedUser
from ..models import Account, AccountCollaborator, EmailDomain


class AccountTestCase(BaseTestCase):
    def setUp(self):
        super(AccountTestCase, self).setUp()
        self.username = 'jpueblo'
        self.password = 'abc123'

        self.user = User.objects.create_user(
            username=self.username,
            email='jpueblo@example.com',
            password=self.password,
            first_name='Juan',
            last_name='Pueblo'
        )

        self.account = Account.personals.create(
            name='Acme', created_by=self.user)

    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(Account._meta.fields), 11)

    def test_create_new_account_sets_unique_slug(self):
        account = Account.personals.create(name='Acme', created_by=self.user)

        self.assertEqual(account.slug, 'acme-2')

    def test_add_email_domains_should_create_email_domains(self):
        self.account.add_email_domains(['example.com', 'acme.com'])

        self.assertEqual(EmailDomain.objects.count(), 2)

    def test_invite_user_should_return_inviteduser_get_or_create_tuple(self):
        data = {
            'email': 'ppueblo@example.com',
            'created_by': self.user
        }

        invited_user_tuple = self.account.invite_user(data)

        invited_user = InvitedUser.objects.get(
            email=data['email'], account=self.account)

        self.assertEqual(invited_user_tuple, (invited_user, True))


class AccountCollaboratorTestCase(BaseTestCase):
    def setUp(self):
        self.username = 'jpueblo'
        self.password = 'abc123'

        self.user = User.objects.create_user(
            username=self.username,
            email='jpueblo@example.com',
            password=self.password,
            first_name='Juan',
            last_name='Pueblo'
        )

        self.account = Account.personals.create(
            name='Acme', created_by=self.user)

    def test_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in model.
        """
        self.assertEqual(len(AccountCollaborator._meta.fields), 6)

    def test_manager_create_owner_should_create_member_with_owner_role(self):
        """
        Tests that manager method create_owner should create
        an AccountMember with the owner role.
        """
        account_member = AccountCollaborator.objects.create_owner(
            account=self.account, user=self.user)

        self.assertTrue(account_member.is_owner)
