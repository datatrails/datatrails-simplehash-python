#!/usr/bin/env python3

""" Module for implementation of simplehash canonicalization"""

from hashlib import sha256
from json import load as json_load
from operator import itemgetter
from sys import stdin as sys_stdin

from bencodepy import encode as binary_encode

V1_FIELDS = {
    "identity",
    "asset_identity",
    "event_attributes",
    "asset_attributes",
    "operation",
    "behaviour",
    "timestamp_declared",
    "timestamp_accepted",
    "timestamp_committed",
    "principal_accepted",
    "principal_declared",
    "confirmation_status",
    "from",
    "tenant_identity",
}


class SimpleHashPendingEventFound(Exception):
    """If PENDING event found"""


class SimpleHashFieldMissing(Exception):
    """If essential field is missing"""


def __check_events(events):
    """Raise exception if any PENDING events found or
    if required keys are missing"""

    for event in events:
        missing = V1_FIELDS.difference(event)
        if missing:
            raise SimpleHashFieldMissing(
                f"Event Identity {event['identity']} has missing field(s) {missing}"
            )
        if event["confirmation_status"] not in ("FAILED", "CONFIRMED"):
            raise SimpleHashPendingEventFound(
                f"Event Identity {event['identity']} has illegal "
                f"confirmation status {event['confirmation_status']}"
            )


def redact_events(events):
    """Form list of sorted (by identity) events only containing necessary fields"""
    return [
        {k: event[k] for k in V1_FIELDS}
        for event in sorted(events, key=itemgetter("identity"))
    ]


def hash_events(response):
    """Generate Simplehash for a given set of events canonicalizing then hashing"""

    __check_events(response["events"])
    redacted_events = redact_events(response["events"])

    # bencode the events which produces the canonical form
    canonicalized_events = binary_encode(redacted_events)

    # Hash the canonicalized events
    return sha256(canonicalized_events).hexdigest()


def main():
    """Reads the response fom the ListEvents query stdin"""

    events_hash = hash_events(json_load(sys_stdin))
    print("SimpleHash", events_hash)


if __name__ == "__main__":  # pragma: no cover
    main()
