from rest_framework import status
from rest_framework.test import APIClient

from ...utils.tests import BaseTestCase, AuthenticatedAPITestCase
from ...accounts.models import Account, EmailDomain
from ...users.serializers import NestedUserSerializer


class ValidateSignupDomainsAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'signup_domains': ['example.com']
        }

        response = self.client.post(
            '/api/v1/auth/signup_domains/validate/', data, format='json')

        expected_response = {
            'signup_domains': ['example.com']
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/v1/auth/signup_domains/validate/')

        expected_response = {
            'error': {
                'signup_domains': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)

    def test_post_blacklisted_domain(self):
        """
        Tests that POST request with blacklisted domain to endpoint
        returns expected error.
        """
        data = {
            'signup_domains': ['gmail.com']
        }

        response = self.client.post(
            '/api/v1/auth/signup_domains/validate/', data, format='json')

        expected_response = {
            'error': {
                'signup_domains': [
                    "gmail.com is an invalid sign-up domain."
                ]
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class CheckSignupDomainAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user()

    def test_post_valid_data(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        account = Account.personals.create(
            name='Acme', allow_signup=True, created_by=self.user)

        email_domain = EmailDomain.objects.create(domain_name='example.com')

        account.email_domains.add(email_domain)

        data = {
            'signup_domain': 'example.com'
        }

        response = self.client.post(
            '/api/v1/auth/signup_domains/check/', data, format='json')

        created_by = NestedUserSerializer(account.created_by).data
        modified_by = NestedUserSerializer(account.modified_by).data

        expected_response = {
            'id': account.id,
            'name': 'Acme',
            'slug': 'acme',
            'logo_color': '',
            'type': 'personal',
            'disqus_shortname': '',
            'created_by': created_by,
            'modified_by': modified_by,
            'date_created': account.date_created,
            'date_modified': account.date_modified,
            'html_url': account.html_url
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_valid_data_no_account_found(self):
        """
        Tests that POST request with valid data to endpoint
        returns expected data.
        """
        data = {
            'signup_domain': 'example.com'
        }

        response = self.client.post(
            '/api/v1/auth/signup_domains/check/', data, format='json')

        expected_response = {}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def test_post_invalid_data(self):
        """
        Tests that POST request with invalid data to endpoint
        returns expected error.
        """
        response = self.client.post('/api/v1/auth/signup_domains/check/')

        expected_response = {
            'error': {
                'signup_domain': ['This field is required.']
            }
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)


class AccountsForUserAPIViewTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super(AccountsForUserAPIViewTestCase, self).setUp()

        self.create_account()

    def test_get_accounts_without_token_should_fail(self):
        self.client = APIClient()
        response = self.client.get('/api/v1/accounts/')

        expected_response = {
            'error': 'Authentication credentials were not provided.',
            'status_code': 401
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, expected_response)

    def test_get_account_with_token_should_work(self):
        response = self.client.get('/api/v1/accounts/')

        created_by = NestedUserSerializer(self.account.created_by).data
        modified_by = NestedUserSerializer(self.account.modified_by).data

        expected_response = [{
            'id': self.account.id,
            'name': 'Acme',
            'slug': 'acme',
            'logo_color': '',
            'type': 'personal',
            'disqus_shortname': '',
            'created_by': created_by,
            'modified_by': modified_by,
            'date_created': self.account.date_created,
            'date_modified': self.account.date_modified,
            'html_url': self.account.html_url
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
