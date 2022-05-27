"""
Tests for the `openstax-oauth-backend` models module.
"""

import json

from social_core.tests.backends.oauth import OAuth2Test
from social_core.exceptions import AuthException


class WPOauth2Test(OAuth2Test):
    backend_path = 'wp_oauth_backend.wp.WPOAuth2'
    base_url = 'https://accounts-dev.openstax.org'
    user_data_url = 'https://accounts-dev.openstax.org/api/user?lpm0073@gmail.com'
    expected_username = 'lpm0073@gmail.com'
    access_token_body = json.dumps({
        'access_token': '547cac21118ae7',
        'token_type': 'bearer',
        'expires_in': 2592000,
        'refresh_token': '00a3aae641658d',
    })
    user_data_body = json.dumps({
        'first_name': 'Lawrence',
        'last_name': 'McDaniel',
        'full_name': 'Lawrence McDaniel',
        'email': 'lpm0073@gmail.com',
        'username': 'lpm0073@gmail.com',
    })

    def test_login(self):
        self.do_login()

    def test_redirect_state_settings(self):
        """
        Tests for the redirect state option.

        From Python Social Auth docs (https://tinyurl.com/psa-redirect-state)

        > For those providers that don't recognise the state parameter, the
        > app can add a redirect_state argument to the redirect_uri to mimic
        > it. Set this value to False if the provider likes to
        > verify the redirect_uri value and this
        > parameter invalidates that check.

        So, when enabling it, we should double check with Trinity
        """
        message = 'Openstax backend PROBABLY do not support this parameter'
        assert not self.backend.REDIRECT_STATE, message

    def test_backend_configs(self):
        # Changing it is probably backward incompatible
        assert self.backend.name == 'openstax'

        assert self.backend.ACCESS_TOKEN_METHOD == 'POST'
        assert self.backend.SCOPE_SEPARATOR == ','

    def test_partial_pipeline(self):
        self.do_partial_pipeline()

    def test_staging_url(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_OPENSTAX_ENVIRONMENT': 'staging',
        })

        assert self.backend.base_url == 'https://accounts-dev.openstax.org'

    def test_production_url(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_OPENSTAX_ENVIRONMENT': 'production',
        })

        assert self.backend.base_url == 'https://accounts.openstax.org'

    def test_default_production_url(self):
        assert self.backend.base_url == 'https://accounts-dev.openstax.org'

    def test_invalid_environment(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_OPENSTAX_ENVIRONMENT': 'dev',
        })

        with self.assertRaises(AuthException):
            print(self.backend.base_url)
