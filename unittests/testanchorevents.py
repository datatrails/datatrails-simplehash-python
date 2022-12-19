"""
Test anchor_events method
"""

from unittest import TestCase, mock

from requests import RequestException

from rkvst_simplehash.v1 import (
    anchor_events,
    SimpleHashFieldError,
    SimpleHashFieldMissing,
    SimpleHashPendingEventFound,
    SimpleHashRequestsError,
)

from .mock_response import MockResponse

# The earliest timestamp_accepted in  any mock event
MIN_ACCEPTED = "2022-10-07 07:01:34Z"

# The latest timestamp_accepted in any mock event
MAX_ACCEPTED = "2022-10-16T13:14:56Z"

# FQDN isn't used anywhere as the requests.get is mocked
FQDN = "app.test.rkvst.io"

# AUTH_TOKEN isn't used anywhere as the requests.get is mocked
AUTH_TOKEN = "dummy auth"


VALID_EVENTS = [
    {
        "identity": (
            "assets/03c60f22-588c-4f12-b3c2-e98c7f2e98a0/"
            "events/409ae05a-183d-4e55-8aa6-889159edefd3"
        ),
        "asset_identity": "assets/03c60f22-588c-4f12-b3c2-e98c7f2e98a0",
        "event_attributes": {"foo": "bar"},
        "asset_attributes": {"fab": "baz"},
        "operation": "Record",
        "behaviour": "RecordEvidence",
        "timestamp_declared": "2022-10-16T13:14:50Z",
        "timestamp_accepted": "2022-10-16T13:14:55Z",
        "timestamp_committed": "2022-10-16T13:14:59Z",
        "principal_declared": {
            "issuer": "https://rkvt.com",
            "subject": "117303158125148247777",
            "display_name": "William Defoe",
            "email": "WilliamDefoe@rkvst.com",
        },
        "principal_accepted": {
            "issuer": "https://rkvt.com",
            "subject": "117303158125148247777",
            "display_name": "William Defoe",
            "email": "WilliamDefoe@rkvst.com",
        },
        "confirmation_status": "CONFIRMED",
        "from": "0xf8dfc073650503aeD429E414bE7e972f8F095e70",
        "tenant_identity": "tenant/0684984b-654d-4301-ad10-a508126e187d",
    },
    {
        "identity": (
            "assets/a987b910-f567-4cca-9869-bbbeb12aec20/"
            "events/936ba508-ee65-426d-8903-52c59cb4655b"
        ),
        "asset_identity": "assets/a987b910-f567-4cca-9869-bbbeb12aec20",
        "event_attributes": {"make": "volvo"},
        "asset_attributes": {"vehicle": "car"},
        "operation": "Record",
        "behaviour": "RecordEvidence",
        "timestamp_declared": "2022-10-07T07:01:30Z",
        "timestamp_accepted": "2022-10-07T07:01:35Z",
        "timestamp_committed": "2022-10-07T07:01:39Z",
        "principal_declared": {
            "issuer": "https://rkvt.com",
            "subject": "227303158125148248888",
            "display_name": "John Cena",
            "email": "JohnCena@rkvst.com",
        },
        "principal_accepted": {
            "issuer": "https://rkvt.com",
            "subject": "227303158125148248888",
            "display_name": "John Cena",
            "email": "JohnCena@rkvst.com",
        },
        "confirmation_status": "CONFIRMED",
        "from": "0xa453a973650503aeD429E414bE7e972f8F095f81",
        "tenant_identity": "tenant/0684984b-654d-4301-ad10-a508126e187d",
    },
]


VALID_EVENT = {
    "identity": (
        "assets/64dc9f7a-9d94-4ee0-835e-9d234e882c9e/"
        "events/97c7825a-a62e-459a-b091-dd85cd7b467e"
    ),
    "asset_identity": "assets/64dc9f7a-9d94-4ee0-835e-9d234e882c9e",
    "behaviour": "RecordEvidence",
    "operation": "Record",
    "confirmation_status": "CONFIRMED",
    "asset_attributes": {},
    "event_attributes": {
        "arc_description": "Safety conformance approved for version 1.6.",
        "arc_evidence": "DVA Conformance Report attached",
        "conformance_report": "blobs/e2a1d16c-03cd-45a1-8cd0-690831df1273",
    },
    "principal_accepted": {
        "display_name": "joe.bloggs@rkvst.com",
        "email": "joe.bloggs@rkvst.com",
        "issuer": "http://server.example.com",
        "subject": "248289761001",
    },
    "principal_declared": {
        "display_name": "",
        "email": "phil.b@synsation.io",
        "issuer": "idp.synsation.io/1234",
        "subject": "phil.b",
    },
    "tenant_identity": "tenant/0dc854f5-5eab-4ad8-9d75-1ea9b24d0db4",
    "timestamp_accepted": "2022-10-14T09:20:51Z",
    "timestamp_committed": "2022-10-14T09:20:51.920717507Z",
    "timestamp_declared": "2019-11-27T14:44:19Z",
    "from": "0x92a2923C46ff3904f8Fb0E80d1f0448AeE10BC9d",
    "block_number": 0,
    "transaction_id": "",
    "transaction_index": 0,
}

PENDING_EVENT = {
    "identity": (
        "assets/12349f7a-9d94-4ee0-835e-34567e882c9e/"
        "events/97c7825a-a62e-459a-b091-4571cd7b467e"
    ),
    "asset_identity": "assets/12349f7a-9d94-4ee0-835e-34567e882c9e",
    "behaviour": "RecordEvidence",
    "operation": "Record",
    "confirmation_status": "PENDING",
    "asset_attributes": {},
    "event_attributes": {
        "arc_description": "Safety conformance approved for version 1.6.",
        "arc_evidence": "DVA Conformance Report attached",
        "conformance_report": "blobs/e2a1d16c-03cd-45a1-8cd0-547189df1273",
    },
    "principal_accepted": {
        "display_name": "joe.bloggs@rkvst.com",
        "email": "joe.bloggs@rkvst.com",
        "issuer": "http://server.example.com",
        "subject": "248289761001",
    },
    "principal_declared": {
        "display_name": "",
        "email": "phil.b@synsation.io",
        "issuer": "idp.synsation.io/1234",
        "subject": "phil.b",
    },
    "tenant_identity": "tenant/0dc854f5-5eab-4ad8-9d75-1ea9b24d0db4",
    "timestamp_accepted": "2022-10-14T09:30:52Z",
    "timestamp_committed": "2022-10-14T09:30:52.920717507Z",
    "timestamp_declared": "2019-11-28T14:44:19Z",
    "from": "0x92a2923C46ff3904f8Fb0E80d1f0448AeE10BC9d",
    "block_number": 0,
    "transaction_id": "",
    "transaction_index": 0,
}

INCOMPLETE_EVENT = {
    "identity": (
        "assets/12349f7a-9d94-4ee0-835e-34567e854678/"
        "events/97c7825a-a62e-459a-b091-4571cd754678"
    ),
    "asset_identity": "assets/12349f7a-9d94-4ee0-835e-34567e854678",
    "behaviour": "RecordEvidence",
    "operation": "Record",
    "confirmation_status": "CONFIRMED",
    "principal_accepted": {
        "display_name": "joe.bloggs@rkvst.com",
        "email": "joe.bloggs@rkvst.com",
        "issuer": "http://server.example.com",
        "subject": "248289761001",
    },
    "principal_declared": {
        "display_name": "",
        "email": "phil.b@synsation.io",
        "issuer": "http://server.example.com",
        "subject": "phil.b",
    },
    "tenant_identity": "tenant/0dc854f5-5eab-4ad8-9d75-1ea9b24d0db4",
    "timestamp_accepted": "2022-10-14T09:30:52Z",
    "timestamp_committed": "2022-10-14T09:30:52.920717507Z",
    "timestamp_declared": "2019-11-28T14:44:19Z",
    "from": "0x92a2923C46ff3904f8Fb0E80d1f0448AeE10BC9d",
    "block_number": 0,
    "transaction_id": "",
    "transaction_index": 0,
}

NO_CONFIRMATION_EVENT = {
    "identity": (
        "assets/12349f7a-9d94-4ee0-835e-34567e882c9e/"
        "events/97c7825a-a62e-459a-b091-4571cd7b467e"
    ),
    "asset_identity": "assets/12349f7a-9d94-4ee0-835e-34567e882c9e",
    "behaviour": "RecordEvidence",
    "operation": "Record",
    "asset_attributes": {},
    "event_attributes": {
        "arc_description": "Safety conformance approved for version 1.6.",
        "arc_evidence": "DVA Conformance Report attached",
        "conformance_report": "blobs/e2a1d16c-03cd-45a1-8cd0-547189df1273",
    },
    "principal_accepted": {
        "display_name": "joe.bloggs@rkvst.com",
        "email": "joe.bloggs@rkvst.com",
        "issuer": "http://server.example.com",
        "subject": "248289761001",
    },
    "principal_declared": {
        "display_name": "",
        "email": "phil.b@synsation.io",
        "issuer": "idp.synsation.io/1234",
        "subject": "phil.b",
    },
    "tenant_identity": "tenant/0dc854f5-5eab-4ad8-9d75-1ea9b24d0db4",
    "timestamp_accepted": "2022-10-14T09:30:52Z",
    "timestamp_committed": "2022-10-14T09:30:52.920717507Z",
    "timestamp_declared": "2019-11-28T14:44:19Z",
    "from": "0x92a2923C46ff3904f8Fb0E80d1f0448AeE10BC9d",
    "block_number": 0,
    "transaction_id": "",
    "transaction_index": 0,
}

# these are deliberately in the wrong order sorted bu=y identity
# so we can check the redact_sorted_events() function reorders them
VALID_EVENTS_RESPONSE = {"events": VALID_EVENTS}
VALID_EVENT0_RESPONSE = {"events": [VALID_EVENTS[0]]}
VALID_EVENT1_RESPONSE = {"events": [VALID_EVENTS[1]]}

VALID_EVENTS_EXPECTED_HASH = (
    "61211c916cd113a1cf424ac729924de46aa6259919825dbdf8ec78c5c14665e2"
)

NO_EVENTS_EXPECTED_HASH = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

PENDING_EVENTS_RESPONSE = {
    "events": [
        PENDING_EVENT,
        VALID_EVENT,
    ]
}

INCOMPLETE_EVENTS_RESPONSE = {
    "events": [
        INCOMPLETE_EVENT,
        VALID_EVENT,
    ]
}

NO_CONFIRMATION_EVENTS_RESPONSE = {
    "events": [
        NO_CONFIRMATION_EVENT,
        VALID_EVENT,
    ]
}
NO_EVENTS_RESPONSE = {
    "events": [],
}


class TestHashEventsV1(TestCase):
    """
    Test anchor_events
    """

    maxDiff = None

    @mock.patch("rkvst_simplehash.v1.requests_get")
    def test_anchor_events_v1(self, mock_get):
        """
        Test anchor_events
        """

        mock_get.return_value = MockResponse(200, **VALID_EVENTS_RESPONSE)

        simplehash = anchor_events(MIN_ACCEPTED, MAX_ACCEPTED, FQDN, AUTH_TOKEN)
        self.assertEqual(
            VALID_EVENTS_EXPECTED_HASH,
            simplehash,
            msg="Hash has incorrect value",
        )

        # check mock was called with our expected request
        self.assertEqual(
            tuple(mock_get.call_args),
            (
                ("https://app.test.rkvst.io/archivist/v2/assets/-/events",),
                {
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer dummy auth",
                    },
                    "params": {
                        "order_by": "SIMPLEHASHV1",
                        "page_size": 10,
                        "proof_mechanism": "SIMPLE_HASH",
                        "timestamp_accepted_before": "2022-10-16T13:14:56Z",
                        "timestamp_accepted_since": "2022-10-07 07:01:34Z",
                    },
                    "timeout": 10,
                },
            ),
            msg="GET method called incorrectly",
        )

    @mock.patch("rkvst_simplehash.v1.requests_get")
    def test_anchor_events_v1_paging(self, mock_get):
        """
        Test anchor_events
        """
        page_size = 1
        params = [
            {
                "order_by": "SIMPLEHASHV1",
                "page_size": page_size,
                "proof_mechanism": "SIMPLE_HASH",
                "timestamp_accepted_before": "2022-10-16T13:14:56Z",
                "timestamp_accepted_since": "2022-10-07 07:01:34Z",
            },
            {"page_token": "next_page_token"},
        ]
        mock_get.side_effect = (
            MockResponse(
                200, **VALID_EVENT0_RESPONSE, next_page_token="next_page_token"
            ),
            MockResponse(200, **VALID_EVENT1_RESPONSE),
        )

        # should be same result as unpaged test
        simplehash = anchor_events(
            MIN_ACCEPTED, MAX_ACCEPTED, FQDN, AUTH_TOKEN, page_size=page_size
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
                    ("https://app.test.rkvst.io/archivist/v2/assets/-/events",),
                    {
                        "headers": {
                            "Content-Type": "application/json",
                            "Authorization": "Bearer dummy auth",
                        },
                        "params": params[i],
                        "timeout": 10,
                    },
                ),
                msg="GET method called incorrectly",
            )

    @mock.patch("rkvst_simplehash.v1.requests_get")
    def test_anchor_events_v1_with_pending_event(self, mock_get):
        """
        Test anchor_events
        """
        mock_get.return_value = MockResponse(200, **PENDING_EVENTS_RESPONSE)

        with self.assertRaises(SimpleHashPendingEventFound):
            dummy = anchor_events(MIN_ACCEPTED, MAX_ACCEPTED, FQDN, AUTH_TOKEN)

    @mock.patch("rkvst_simplehash.v1.requests_get")
    def test_anchor_events_v1_with_no_events(self, mock_get):
        """
        Test anchor_events with no events
        """
        mock_get.return_value = MockResponse(200, **NO_EVENTS_RESPONSE)

        simplehash = anchor_events(MIN_ACCEPTED, MAX_ACCEPTED, FQDN, AUTH_TOKEN)
        self.assertEqual(
            NO_EVENTS_EXPECTED_HASH,
            simplehash,
            msg="Hash has incorrect value",
        )

    @mock.patch("rkvst_simplehash.v1.requests_get")
    def test_anchor_events_v1_with_missing_events(self, mock_get):
        """
        Test anchor_events with missing events
        """
        mock_get.return_value = MockResponse(200)

        with self.assertRaises(SimpleHashFieldError):
            dummy = anchor_events(MIN_ACCEPTED, MAX_ACCEPTED, FQDN, AUTH_TOKEN)

    @mock.patch("rkvst_simplehash.v1.requests_get")
    def test_anchor_events_v1_with_incomplete_event(self, mock_get):
        """
        Test anchor_events with incomplete event
        """
        mock_get.return_value = MockResponse(200, **INCOMPLETE_EVENTS_RESPONSE)

        with self.assertRaises(SimpleHashFieldMissing):
            dummy = anchor_events(MIN_ACCEPTED, MAX_ACCEPTED, FQDN, AUTH_TOKEN)

    @mock.patch("rkvst_simplehash.v1.requests_get")
    def test_anchor_events_v1_with_no_confirmation_status(self, mock_get):
        """
        Test anchor_events with no confirmation status
        """
        mock_get.return_value = MockResponse(200, **NO_CONFIRMATION_EVENTS_RESPONSE)

        with self.assertRaises(SimpleHashFieldMissing):
            dummy = anchor_events(MIN_ACCEPTED, MAX_ACCEPTED, FQDN, AUTH_TOKEN)

    @mock.patch("rkvst_simplehash.v1.requests_get")
    def test_anchor_events_v1_with_requests_exception(self, mock_get):
        """
        Test anchor_events
        """
        mock_get.return_value = MockResponse(
            200, exception=RequestException, **PENDING_EVENTS_RESPONSE
        )

        with self.assertRaises(SimpleHashRequestsError):
            dummy = anchor_events(MIN_ACCEPTED, MAX_ACCEPTED, FQDN, AUTH_TOKEN)
