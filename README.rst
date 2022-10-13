
.. _readme:

RKVST Simplehash in python
===========================

Prescribed python code that defines the hashing algorithm for DLT Anchoring.

Support
=======

This package currently is tested against Python versions 3.7,3.8,3.9 and 3.10.

The current default version is 3.7 - this means that this package will not
use any features specific to versions 3.8 and later.

After End of Life of a particular Python version, support is offered on a best effort
basis. We may ask you to update your Python version to help solve the problem,
if it cannot be reasonably resolved in your current version.

Installation
=============

Use standard python pip utility:

.. code:: bash

    python3 -m pip install rkvst-simplehash

If your version of python3 is too old an error of this type or similar will be emitted:

.. note::

    ERROR: Could not find a version that satisfies the requirement rkvst-simplehash (from versions: none)
    ERROR: No matching distribution found for rkvst-simplehash

Example
=============

You can then use the code to recreate the simple hash of a list of SIMPLE_HASH events from RKVST.

.. code:: python

    """From a list of events.
    """

    from rkvst_simplehash.v1 import hash_events

    # if any pending events a SimpleHashPendingEventFound error will be thrown
    # if any of the events do not contain the required field then a SimpleHashFieldMissing error will be thrown

    simplehash = hash_events(events)


Command Line
------------

This functionality is also available on the cmdline. Execute the simplehash query using curl and pip to the
rkvst_simplehashv1 command or the v1.py script.

Installing locally:
....................

Execute this after cloning the repo.

.. code:: bash

    python3 -m pip install bencode.py~=4.0

    URL="https://app.rkvst.io/archivist/v2/assets/-/events"
    SINCE=timestamp_accepted_since=2022-10-19T00:00:00Z
    BEFORE=timestamp_accepted_before=2022-10-26T00:00:00Z
    BEARER_TOKEN_FILE=credentials/token

    curl -s -X GET \
         -H "@$BEARER_TOKEN_FILE" \
         "$URL?proof_mechanism=SIMPLE_HASH&${SINCE}&${BEFORE}" | rkvst_simplehash/v1.py


Using a virtual env and published wheel:
........................................

This can be executed anywhere using a virtualenv and published wheel.

.. code:: bash

    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install rkvst_simplehash

    URL="https://app.rkvst.io/archivist/v2/assets/-/events"
    SINCE=timestamp_accepted_since=2022-10-19T00:00:00Z
    BEFORE=timestamp_accepted_before=2022-10-26T00:00:00Z
    BEARER_TOKEN_FILE=credentials/token

    curl -s -X GET \
         -H "@$BEARER_TOKEN_FILE" \
         "$URL?proof_mechanism=SIMPLE_HASH&${SINCE}&${BEFORE}" | rkvst_simplehashv1

    deactivate
    rm -rf simplehash-venv

