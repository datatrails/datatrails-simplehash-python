"""
Test get_auth_token method
"""

from unittest import TestCase, mock

from requests import RequestException
from rkvst_simplehash.v1 import get_auth_token, SimpleHashRequestsError

from .mock_response import MockResponse

FQDN = "app.rkvst-test.io"
CLIENT_ID = "client_id-2f78-4fa0-9425-d59314845bc5"
CLIENT_SECRET = "client_secret-388f5187e32d930d83"
ACCESS_TOKEN = "access_token-xbXATAWrEpepR7TklOxRB-yud92AsD6DGGasiEGN7MZKT0AIQ4Rw9s"
REQUEST = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

RESPONSE = {
    "access_token": ACCESS_TOKEN,
    "expires_in": 660,
    "token_type": "Bearer",
}


class TestGetAuthToken(TestCase):
    """
    Test get_auth_token
    """

    maxDiff = None

    @mock.patch("rkvst_simplehash.v1.requests_post")
    def test_get_auth_token_v1(self, mock_post):
        """
        Test anchor_events
        """

        mock_post.return_value = MockResponse(200, **RESPONSE)
        token = get_auth_token(
            FQDN,
            CLIENT_ID,
            CLIENT_SECRET,
        )
        args, kwargs = mock_post.call_args
        self.assertEqual(
            args,
            ("https://app.rkvst-test.io/archivist/iam/v1/appidp/token",),
            msg="CREATE method args called incorrectly",
        )
        self.assertEqual(
            kwargs,
            {
                "data": REQUEST,
                "timeout": 10,
            },
            msg="CREATE method kwargs called incorrectly",
        )
        self.assertEqual(
            token,
            ACCESS_TOKEN,
            msg="TOKEN method called incorrectly",
        )

    @mock.patch("rkvst_simplehash.v1.requests_post")
    def test_get_auth_token_request_exception_v1(self, mock_post):
        """
        Test anchor_events
        """

        mock_post.return_value = MockResponse(
            400, exception=RequestException, **RESPONSE
        )

        with self.assertRaises(SimpleHashRequestsError):
            dummy = get_auth_token(
                FQDN,
                CLIENT_ID,
                CLIENT_SECRET,
            )
