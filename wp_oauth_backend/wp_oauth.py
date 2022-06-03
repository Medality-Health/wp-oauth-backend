import json
from urllib.parse import urlencode
from urllib.request import urlopen
from social_core.backends.oauth import BaseOAuth2
from django.conf import settings

from logging import getLogger
logger = getLogger(__name__)

PROBLEMATIC_USERS = []
class WPOAuth2(BaseOAuth2):

    """Rover OAuth authentication backend"""
    name = 'wp-oauth2'

    base_url = settings.WPOAUTH_BACKEND_BASE_URL
    CLIENT_ID = settings.WPOAUTH_BACKEND_CLIENT_ID
    CLIENT_SECRET = settings.WPOAUTH_BACKEND_CLIENT_SECRET    
    SOCIAL_AUTH_SANITIZE_REDIRECTS = False
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = []
    SCOPE_SEPARATOR = ','

    @property
    def AUTHORIZATION_URL(self) -> str:
        return f"{self.base_url}/oauth/authorize"

    @property
    def ACCESS_TOKEN_URL(self) -> str:
        return f"{self.base_url}/oauth/token"

    @property
    def USER_QUERY(self) -> str:
        return f"{self.base_url}/oauth/me"

    def get_user_details(self, response):
        """Return user details from the WP account"""
        user_details = {
            'id': int(response.get('ID')),
            'username': response.get('user_login'),
            'email': response.get('user_email'),
            'fullname': response.get('display_name'),
        }
        logger.info('get_user_details() -  {}'.format(user_details))
        if response.get('email') in PROBLEMATIC_USERS:
            logger.warning('get_user_details() -  user is a PROBLEMATIC_USER. disabling output')
            return None

        return user_details

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = f'{self.USER_QUERY}?' + urlencode({
            'access_token': access_token
        })

        try:
            return json.loads(self.urlopen(url))
        except ValueError:
            return None

    def urlopen(self, url):
        return urlopen(url).read().decode("utf-8")

    def get_user_id(self, details, response):
        return details['id']

    def get_username(self, strategy, details, backend, user=None, *args, **kwargs):
        return details['username']

    def get_key_and_secret(self):
        return (self.CLIENT_ID, self.CLIENT_SECRET)
