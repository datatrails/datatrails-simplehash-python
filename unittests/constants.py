"""
Constants
"""

# The earliest timestamp_accepted in  any mock event
MIN_ACCEPTED = "2022-10-07 07:01:34Z"

# The latest timestamp_accepted in any mock event
MAX_ACCEPTED = "2022-10-16T13:14:56Z"

URL = "https://app.datatrails-test.ai"
PATH = "archivist/v2/assets/-/events"
PUBLICPATH = "archivist/v2/publicassets/-/events"
API_QUERY = (
    f"{URL}/{PATH}"
    "?proof_mechanism=SIMPLE_HASH"
    f"&timestamp_accepted_since={MIN_ACCEPTED}"
    f"&timestamp_accepted_before={MAX_ACCEPTED}"
    "&order_by=SIMPLEHASHV1"
)
API_QUERY_PUBLIC = (
    f"{URL}/{PUBLICPATH}"
    "?proof_mechanism=SIMPLE_HASH"
    f"&timestamp_accepted_since={MIN_ACCEPTED}"
    f"&timestamp_accepted_before={MAX_ACCEPTED}"
    "&order_by=SIMPLEHASHV1"
)

# dummy auth token
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

VALID_PUBLIC_EVENTS = [
    {
        "identity": (
            "publicassets/03c60f22-588c-4f12-b3c2-e98c7f2e98a0/"
            "events/409ae05a-183d-4e55-8aa6-889159edefd3"
        ),
        "asset_identity": "publicassets/03c60f22-588c-4f12-b3c2-e98c7f2e98a0",
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
            "publicassets/a987b910-f567-4cca-9869-bbbeb12aec20/"
            "events/936ba508-ee65-426d-8903-52c59cb4655b"
        ),
        "asset_identity": "publicassets/a987b910-f567-4cca-9869-bbbeb12aec20",
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
}

# these are deliberately in the wrong order sorted bu=y identity
# so we can check the redact_sorted_events() function reorders them
VALID_EVENTS_RESPONSE = {"events": VALID_EVENTS}
VALID_PUBLIC_EVENTS_RESPONSE = {"events": VALID_PUBLIC_EVENTS}
VALID_EVENT0_RESPONSE = {"events": [VALID_EVENTS[0]]}
VALID_EVENT1_RESPONSE = {"events": [VALID_EVENTS[1]]}

VALID_EVENTS_EXPECTED_HASH = (
    "61211c916cd113a1cf424ac729924de46aa6259919825dbdf8ec78c5c14665e2"
)

VALID_PUBLIC_EVENTS_EXPECTED_HASH = (
    "63ab884c8d59d0f508c3f5f90c6bc175eb173c8d8ec12aa811e3b084543c1b4f"
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
