import unittest
from flood.utils import body_validations


class TestStringMethods(unittest.TestCase):

    def test_group_validations(self):
        body_validations.validate_group(
            {
                'name': 'jonas',
                'requst_id': 'jonas'
            }
        )

    def test_message_validations(self):
        body_validations.validate_message(
            {
                'text': 'jonas'

            }
        )

    def test_user_validations(self):
        body_validations.validate_user(
            {
                'email': 'jonas',
                'pswd': 'jonas',
                'name': 'jonas'
            }
        )

    def test_geolocation_validations(self):
        body_validations.validate_geolocation(
            {
                'latitude': 1.1,
                'longitude': 2.2
            }
        )

    def test_auth_validations(self):
        body_validations.validate_auth(
            {
                'email': 'jonas',
                'pswd': 'jonas'
            }
        )



