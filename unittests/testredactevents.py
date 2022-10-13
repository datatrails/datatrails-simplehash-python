"""
Test redact_sorted_events method
"""

from unittest import TestCase


from rkvst_simplehash.v1 import (
    redact_events,
)

from .testhashevents import VALID_EVENTS

REDACTED_EVENT = {
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
}

REDACTED_EVENT1 = {
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
}


# should be sorted by identity
REDACTED_EVENTS = [
    REDACTED_EVENT1,
    REDACTED_EVENT,
]


class TestRedactEventsV1(TestCase):
    """
    Test redacted_events
    """

    maxDiff = None

    def test_redact_events_v1(self):
        """
        Test redacted_events
        """
        redacted_events = redact_events(VALID_EVENTS["events"])
        self.assertEqual(
            REDACTED_EVENTS,
            redacted_events,
            msg="redacted_events has incorrect order",
        )
