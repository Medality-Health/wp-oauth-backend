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
    name = 'roverbyopenstax'

    CLIENT_ID = settings.WPOAUTH_BACKEND_CLIENT_ID
    CLIENT_SECRET = settings.WPOAUTH_BACKEND_CLIENT_SECRET    
    USER_QUERY = 'https://roverbyopenstax.org/o/api/user_data?'
    USERS_QUERY = 'https://roverbyopenstax.org/o/api/users?'
    SOCIAL_AUTH_SANITIZE_REDIRECTS = False
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = []
    SCOPE_SEPARATOR = ','

    @property
    def AUTHORIZATION_URL(self):
        return f"{self.base_url}/oauth/authorize"

    @property
    def ACCESS_TOKEN_URL(self):
        return f"{self.base_url}/oauth/token"

    def get_user_details(self, response):
        """Return user details from openstax account's"""
        contact_infos = response.get('contact_infos')

        id = str(response.get('id'))

        user_details = {
            'id':  id,
            'username': response.get('username'),
            'email': response.get('email'),
            'first_name': response.get('first_name'),
            'last_name': response.get('last_name'),
            'fullname': response.get('first_name') + ' ' + response.get('last_name'),
            'self_reported_role': response.get('self_reported_role', 'unknown_role'),
            'self_reported_school': response.get('self_reported_school', 'unknown_school'),
            'school_type': response.get('school_type', 'unknown_school_type'),
            'faculty_status': response.get('faculty_status', 'no_faculty_info'),
            }
        logger.info('get_user_details() -  {}'.format(user_details))
        if response.get('email') in PROBLEMATIC_USERS:
            logger.warning('get_user_details() -  user is a PROBLEMATIC_USER. disabling output')
            return None

        return user_details

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = self.USER_QUERY + urlencode({
            'access_token': access_token
        })

        try:
            return json.loads(self.urlopen(url))
        except ValueError:
            return None

    @property
    def base_url(self):
        return settings.WPOAUTH_BACKEND_BASE_URL

    def urlopen(self, url):
        return urlopen(url).read().decode("utf-8")

    def get_user_id(self, details, response):
        return details['id']

    def get_username(self, strategy, details, backend, user=None, *args, **kwargs):
        return details['username']

    def get_key_and_secret(self):
        return (self.CLIENT_ID, self.CLIENT_SECRET)
