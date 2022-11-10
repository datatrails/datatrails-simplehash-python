#!/usr/bin/env python3

""" Module for implementation of simplehash canonicalization"""

from hashlib import sha256
from json import load as json_load
from operator import itemgetter
from sys import stdin as sys_stdin

from bencodepy import encode as binary_encode

import requests

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


class ArchivistBadFieldError(Exception):
    """Incorrect field name in list() method"""

class SimpleHashPendingEventFound(Exception):
    """If PENDING event found"""


class SimpleHashFieldMissing(Exception):
    """If essential field is missing"""


def __check_event(event):
    """Raise exception if any PENDING events found or
    if required keys are missing"""

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


def redact_event(event):
    """Form an event only containing necessary fields"""
    return  {k: event[k] for k in V1_FIELDS}


def list_events(start_time, end_time, auth_token):
        """GET method (REST) with params string
        Lists events that match the params dictionary.
        If page size is specified return the list of records in batches of page_size
        until next_page_token in response is null.
        If page size is unspecified return up to the internal limit of records.
        (different for each endpoint)
        Args:
            start_time (string): rfc3339 formatted datetime string of the start date of the time window of events
            end_time (string): rfc3339 formatted datetime string of the end date of the time window of events
            auth_token (string): authorization token to be able to call the list events api
        Returns:
            iterable that lists events
        Raises:
            ArchivistBadFieldError: field has incorrect value.
        """

        #fqdn = "app.rkvst.io"
        fqdn = "app.dev-jgough-0.wild.jitsuin.io"

        url = f"https://{fqdn}/archivist/v2/assets/-/events"
        params = {
            "proof_mechanism": "SIMPLE_HASH",
            "timestamp_accepted_since": start_time,
            "timestamp_accepted_before": end_time,
            "page_size": 10,
            "order_by": "SIMPLEHASHV1"
        }
        headers = {
            'Content-Type':'application/json',
            "Authorization": f"Bearer {auth_token}"
        }

        while True:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            try:
                events = data["events"]
            except KeyError as ex:
                raise ArchivistBadFieldError(f"No events found") from ex

            for event in events:
                yield event

            page_token = data.get("next_page_token")
            if not page_token:
                break

            params = {"page_token": page_token}


def hash_events(start_time, end_time, auth_token):
    """Generate Simplehash for a given set of events canonicalizing then hashing"""

    hasher = sha256()

    # for each event
    for event in list_events(start_time, end_time, auth_token):

        __check_event(event)
        redacted_event = redact_event(event)

        # bencode the events, this orders dictionary keys
        bencoded_event = binary_encode(redacted_event)

        # add the event to the sha256 hash
        hasher.update(bencoded_event)

    # return the complete hash
    return hasher.hexdigest()


def main():
    """Reads the response fom the ListEvents query stdin"""

    events_hash = hash_events(json_load(sys_stdin))
    print("SimpleHash", events_hash)


if __name__ == "__main__":  # pragma: no cover
    main()
