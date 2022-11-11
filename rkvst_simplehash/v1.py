#!/usr/bin/env python3

""" Module for implementation of simplehash canonicalization"""

from hashlib import sha256
from json import load as json_load
from operator import itemgetter
from sys import stdin as sys_stdin

from bencodepy import encode as binary_encode

import requests
import argparse

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


class SimpleHashClientAuthError(Exception):
    """If either client id or secret, or both are missing"""
class SimpleHashFieldError(Exception):
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


def list_events(start_time, end_time, fqdn, auth_token):
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
                raise SimpleHashFieldError(f"No events found") from ex

            for event in events:
                yield event

            page_token = data.get("next_page_token")
            if not page_token:
                break

            params = {"page_token": page_token}


def anchor_events(start_time, end_time, fqdn, auth_token):
    """Generate Simplehash for a given set of events canonicalizing then hashing"""

    hasher = sha256()

    # for each event
    for event in list_events(start_time, end_time, fqdn, auth_token):

        __check_event(event)

        # only accept the correct fields on the event
        redacted_event = redact_event(event)

        # bencode the event, this orders dictionary keys
        bencoded_event = binary_encode(redacted_event)

        # add the event to the sha256 hash
        hasher.update(bencoded_event)

    # return the complete hash
    return hasher.hexdigest()


def get_auth_token(fqdn, client_id, client_secret):
    """
    get_auth_token gets an auth token from an app registration, given its client id and secret
    """

    url = f"https://{fqdn}/archivist/iam/v1/appidp/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url, data=params)
    data = response.json()

    auth_token = data["access_token"]
    return auth_token


def main():
    """Creates an anchor given the start time, end time and auth token"""

    parser = argparse.ArgumentParser(description="Create simple hash anchor.")

    parser.add_argument("--start-time", type=str, help="the start time of the time window to anchor events, formatted as an rfc3339 formatted datetime string.")
    parser.add_argument("--end-time", type=str, help="the end time of the time window to anchor events, formatted as an rfc3339 formatted datetime string.")

    parser.add_argument("--fqdn", type=str, help="the fqdn for the url to list the events in the anchor time window", default="app.rkvst.io")

    # auth
    parser.add_argument("--auth-token-file", type=str, help="filepath to the stored auth token within a file")

    # client id + secret auth
    parser.add_argument("--client-id", type=str, help="client id for an app registration to gain auth, ignored if --auth-token-file is set")
    parser.add_argument("--client-secret-file", type=str, help="filepath to the stored client secret for an app registration to gain auth, ignred if --auth-token-file is set")
    args = parser.parse_args()

    if args.auth_token_file:
        with open(args.auth_token_file) as file:

            # get auth token
            auth_token = str(file.read()).strip('\n')


            anchor = anchor_events(args.start_time, args.end_time, args.fqdn, auth_token)
            print(anchor)
            return

    if args.client_id is None or args.client_secret_file is None:
        raise SimpleHashClientAuthError("'--client-id' and '--client-secret-file' need to be set.")

    # we don't have the auth token file, but we have a client id and secret
    #  so attempt to get the auth token via client id and secret
    with open(args.client_secret_file) as file:

        # get auth token
        client_secret = str(file.read()).strip('\n')
        auth_token = get_auth_token(args.fqdn, args.client_id, client_secret)


        anchor = anchor_events(args.start_time, args.end_time, args.fqdn, auth_token)
        print(anchor)
        return

if __name__ == "__main__":  # pragma: no cover
    main()
