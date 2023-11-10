"""
Test anchor_events method
"""

from unittest import TestCase, mock

from requests import RequestException

from datatrails_simplehash.v2 import (
    DEFAULT_PAGE_SIZE,
    TIMEOUT,
    SimpleHashFieldError,
    SimpleHashFieldMissing,
    SimpleHashPendingEventFound,
    SimpleHashRequestsError,
)

from datatrails_simplehash import v2

from .mock_response import MockResponse

from .constants import (
    API_QUERY,
    API_QUERY_PUBLIC,
    AUTH_TOKEN,
    VALID_EVENTS_RESPONSE,
    VALID_PUBLIC_EVENTS_RESPONSE,
    VALID_EVENT0_RESPONSE,
    VALID_EVENT1_RESPONSE,
    VALID_EVENTS_EXPECTED_HASH,
    VALID_PUBLIC_EVENTS_EXPECTED_HASH,
    NO_EVENTS_EXPECTED_HASH,
    PENDING_EVENTS_RESPONSE,
    INCOMPLETE_EVENTS_RESPONSE,
    NO_CONFIRMATION_EVENTS_RESPONSE,
    NO_EVENTS_RESPONSE,
)


class TestHashEventsV2(TestCase):
    """
    Test anchor_events for v2 schema
    """

    maxDiff = None

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v2(self, mock_get):
        """
        Test anchor_events
        """

        mock_get.return_value = MockResponse(200, **VALID_EVENTS_RESPONSE)

        simplehash = v2.anchor_events(API_QUERY, auth_token=AUTH_TOKEN)
        self.assertEqual(
            VALID_EVENTS_EXPECTED_HASH,
            simplehash,
            msg="Hash has incorrect value",
        )

        # check mock was called with our expected request
        self.assertEqual(
            tuple(mock_get.call_args),
            (
                (f"{API_QUERY}&page_size={DEFAULT_PAGE_SIZE}",),
                {
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer dummy auth",
                    },
                    "params": None,
                    "timeout": TIMEOUT,
                },
            ),
            msg="GET method called incorrectly",
        )

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v2_public(self, mock_get):
        """
        Test anchor_events
        """

        mock_get.return_value = MockResponse(200, **VALID_PUBLIC_EVENTS_RESPONSE)

        simplehash = v2.anchor_events(API_QUERY_PUBLIC)
        self.assertEqual(
            VALID_PUBLIC_EVENTS_EXPECTED_HASH,
            simplehash,
            msg="Hash has incorrect value",
        )

        # check mock was called with our expected request
        self.assertEqual(
            tuple(mock_get.call_args),
            (
                (f"{API_QUERY_PUBLIC}&page_size={DEFAULT_PAGE_SIZE}",),
                {
                    "headers": {
                        "Content-Type": "application/json",
                    },
                    "params": None,
                    "timeout": TIMEOUT,
                },
            ),
            msg="GET method called incorrectly",
        )

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v2_paging(self, mock_get):
        """
        Test anchor_events
        """
        page_size = 1
        params = [
            None,
            {"page_token": "next_page_token"},
        ]
        mock_get.side_effect = (
            MockResponse(
                200, **VALID_EVENT0_RESPONSE, next_page_token="next_page_token"
            ),
            MockResponse(200, **VALID_EVENT1_RESPONSE),
        )

        # should be same result as unpaged test
        simplehash = v2.anchor_events(
            API_QUERY, auth_token=AUTH_TOKEN, page_size=page_size
        )
        self.assertEqual(
            VALID_EVENTS_EXPECTED_HASH,
            simplehash,
            msg="Hash has incorrect value",
        )

        # check mock was called with our expected request
        for i, a in enumerate(mock_get.call_args_list):
            self.assertEqual(
                tuple(a),
                (
                    (f"{API_QUERY}&page_size=1",),
                    {
                        "headers": {
                            "Content-Type": "application/json",
                            "Authorization": "Bearer dummy auth",
                        },
                        "params": params[i],
                        "timeout": TIMEOUT,
                    },
                ),
                msg="GET method called incorrectly",
            )

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v_with_pending_event(self, mock_get):
        """
        Test anchor_events
        """
        mock_get.return_value = MockResponse(200, **PENDING_EVENTS_RESPONSE)

        with self.assertRaises(SimpleHashPendingEventFound):
            dummy = v2.anchor_events(API_QUERY, auth_token=AUTH_TOKEN)

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v2_with_no_events(self, mock_get):
        """
        Test anchor_events with no events
        """
        mock_get.return_value = MockResponse(200, **NO_EVENTS_RESPONSE)

        simplehash = v2.anchor_events(API_QUERY, auth_token=AUTH_TOKEN)
        self.assertEqual(
            NO_EVENTS_EXPECTED_HASH,
            simplehash,
            msg="Hash has incorrect value",
        )

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v2_with_missing_events(self, mock_get):
        """
        Test anchor_events with missing events
        """
        mock_get.return_value = MockResponse(200)

        with self.assertRaises(SimpleHashFieldError):
            dummy = v2.anchor_events(API_QUERY, auth_token=AUTH_TOKEN)

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v2_with_incomplete_event(self, mock_get):
        """
        Test anchor_events with incomplete event
        """
        mock_get.return_value = MockResponse(200, **INCOMPLETE_EVENTS_RESPONSE)

        with self.assertRaises(SimpleHashFieldMissing):
            dummy = v2.anchor_events(API_QUERY, auth_token=AUTH_TOKEN)

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v2_with_no_confirmation_status(self, mock_get):
        """
        Test anchor_events with no confirmation status
        """
        mock_get.return_value = MockResponse(200, **NO_CONFIRMATION_EVENTS_RESPONSE)

        with self.assertRaises(SimpleHashFieldMissing):
            dummy = v2.anchor_events(API_QUERY, auth_token=AUTH_TOKEN)

    @mock.patch("datatrails_simplehash.v2.requests_get")
    def test_anchor_events_v2_with_requests_exception(self, mock_get):
        """
        Test anchor_events
        """
        mock_get.return_value = MockResponse(
            200, exception=RequestException, **PENDING_EVENTS_RESPONSE
        )

        with self.assertRaises(SimpleHashRequestsError):
            dummy = v2.anchor_events(API_QUERY, auth_token=AUTH_TOKEN)
