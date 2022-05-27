"""
Tests for the `wp-oauth-backend` models module.
"""

import json

from social_core.tests.backends.oauth import OAuth2Test
from social_core.exceptions import AuthException

DEV_BASE_URL = 'https://dev.mrionlinedev.com'

class WPOauth2Test(OAuth2Test):
    backend_path = 'wp_oauth_backend.wpoauth.WPOAuth2'
    base_url = DEV_BASE_URL
    user_data_url = f'{DEV_BASE_URL}/api/user?jcohen@mrionline.com'
    expected_username = 'jcohen@mrionline.com'
    access_token_body = json.dumps({
        'access_token': '547cac21118ae7',
        'token_type': 'bearer',
        'expires_in': 2592000,
        'refresh_token': '00a3aae641658d',
    })
    user_data_body = json.dumps({
        'first_name': 'Jeff',
        'last_name': 'Cohen',
        'full_name': 'Jeff Cohen',
        'email': 'jcohen@mrionline.com',
        'username': 'jcohen@mrionline.com',
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
        """
        message = 'WPOAuth2 backend PROBABLY does not support this parameter'
        assert not self.backend.REDIRECT_STATE, message

    def test_backend_configs(self):
        # Changing it is probably backward incompatible
        assert self.backend.name == 'wpoauth2'

        assert self.backend.ACCESS_TOKEN_METHOD == 'POST'
        assert self.backend.SCOPE_SEPARATOR == ','

    def test_partial_pipeline(self):
        self.do_partial_pipeline()

    def test_dev_url(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_WPOAUTH2_ENVIRONMENT': 'development',
        })

        assert self.backend.base_url == 'https://dev.mrionlinedev.com'

    def test_staging_url(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_WPOAUTH2_ENVIRONMENT': 'staging',
        })

        assert self.backend.base_url == 'https://staging.mrionlinedev.com'

    def test_production_url(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_WPOAUTH2_ENVIRONMENT': 'production',
        })

        assert self.backend.base_url == 'https://mrionline.com'

    def test_default_production_url(self):
        assert self.backend.base_url == 'https://mrionline.com'

    def test_invalid_environment(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_WPOAUTH2_ENVIRONMENT': 'unkown',
        })

        with self.assertRaises(AuthException):
            print(self.backend.base_url)
