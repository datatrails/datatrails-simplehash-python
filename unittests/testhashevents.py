"""
Test hash_events method
"""

from io import StringIO
from json import dumps as json_dumps
from unittest import TestCase, mock

from rkvst_simplehash.v1 import (
    anchor_events,
    main,
    SimpleHashFieldMissing,
    SimpleHashPendingEventFound,
)

# The earliest timestamp_accepted in  any mock event
MIN_ACCEPTED = "2022-10-14T09:20:51Z"

# The latest timestamp_accepted in any mock event
MAX_ACCEPTED = "2022-10-14T09:30:52Z"

def add_second(timestamp, seconds=1):
    pass

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
        "display_name": "stunt-idp@jitsuin.com",
        "email": "stunt-idp@jitsuin.com",
        "issuer": "stunt-idp@jitsuin.com",
        "subject": "stunt-idp@jitsuin.com",
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
VALID_EVENT1 = {
    "identity": (
        "assets/64dc9f7a-9d94-4ee0-835e-34567e882c9e/"
        "events/1234825a-a62e-459a-b091-4571cd7b467e"
    ),
    "asset_identity": "assets/64dc9f7a-9d94-4ee0-835e-34567e882c9e",
    "behaviour": "RecordEvidence",
    "operation": "Record",
    "confirmation_status": "CONFIRMED",
    "asset_attributes": {},
    "event_attributes": {
        "arc_description": "Safety conformance approved for version 1.6.",
        "arc_evidence": "DVA Conformance Report attached",
        "conformance_report": "blobs/e2a1d16c-03cd-45a1-8cd0-547189df1273",
    },
    "principal_accepted": {
        "display_name": "stunt-idp@jitsuin.com",
        "email": "stunt-idp@jitsuin.com",
        "issuer": "stunt-idp@jitsuin.com",
        "subject": "stunt-idp@jitsuin.com",
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
        "display_name": "stunt-idp@jitsuin.com",
        "email": "stunt-idp@jitsuin.com",
        "issuer": "stunt-idp@jitsuin.com",
        "subject": "stunt-idp@jitsuin.com",
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
        "display_name": "stunt-idp@jitsuin.com",
        "email": "stunt-idp@jitsuin.com",
        "issuer": "stunt-idp@jitsuin.com",
        "subject": "stunt-idp@jitsuin.com",
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
        "display_name": "stunt-idp@jitsuin.com",
        "email": "stunt-idp@jitsuin.com",
        "issuer": "stunt-idp@jitsuin.com",
        "subject": "stunt-idp@jitsuin.com",
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
VALID_EVENTS = {
    "events": [
        VALID_EVENT,
        VALID_EVENT1,
    ]
}

VALID_EVENTS_EXPECTED_HASH = (
    "70717a0d0504c1315e73662e04d6f479354c35c0acfefe8adcea5e8108397570"
)

NO_EVENTS_EXPECTED_HASH = (
    "61098a4bf2a5e216533e5f2994d8f290308b310f2efa046548a96302afe412ea"
)

PENDING_EVENTS = {
    "events": [
        PENDING_EVENT,
        VALID_EVENT,
        VALID_EVENT1,
    ]
}

INCOMPLETE_EVENTS = {
    "events": [
        INCOMPLETE_EVENT,
        VALID_EVENT,
        VALID_EVENT1,
    ]
}

NO_CONFIRMATION_EVENTS = {
    "events": [
        NO_CONFIRMATION_EVENT,
        VALID_EVENT,
        VALID_EVENT1,
    ]
}


class TestHashEventsV1(TestCase):
    """
    Test hash_events
    """

    maxDiff = None

    def test_hash_events_v1(self):
        """
        Test hash_events
        """
        simplehash = anchor_events(VALID_EVENTS)
        self.assertEqual(
            VALID_EVENTS_EXPECTED_HASH,
            simplehash,
            msg="Hash has incorrect value",
        )

    def test_hash_events_v1_with_pending_event(self):
        """
        Test hash_events
        """
        with self.assertRaises(SimpleHashPendingEventFound):
            dummy = hash_events(PENDING_EVENTS)

    def test_hash_events_v1_with_no_events(self):
        """
        Test hash_events with no events
        """
        simplehash = hash_events({"events": []})
        self.assertEqual(
            NO_EVENTS_EXPECTED_HASH,
            simplehash,
            msg="Hash has incorrect value",
        )

    def test_hash_events_v1_with_incomplete_event(self):
        """
        Test hash_events with incomplete event
        """
        with self.assertRaises(SimpleHashFieldMissing):
            dummy = hash_events(INCOMPLETE_EVENTS)

    def test_hash_events_v1_with_no_confirmation_status(self):
        """
        Test hash_events with no confirmation status
        """
        with self.assertRaises(SimpleHashFieldMissing):
            dummy = hash_events(NO_CONFIRMATION_EVENTS)

    def test_hash_events_v1_main(self):
        """
        Test hash_events main entry point
        """
        valid_events_string = json_dumps(VALID_EVENTS)
        with mock.patch(
            "rkvst_simplehash.v1.sys_stdin", StringIO(valid_events_string)
        ), mock.patch("builtins.print") as mock_print:
            main()
            mock_print.assert_called_with("SimpleHash", VALID_EVENTS_EXPECTED_HASH)
