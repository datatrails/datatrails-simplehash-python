"""
Test redact_sorted_events method
"""

from unittest import TestCase


from rkvst_simplehash.v2 import (
    redact_event,
)

from .constants import REDACTED_EVENT, VALID_EVENT


class TestRedactEventV2(TestCase):
    """
    Test redacted_event
    """

    maxDiff = None

    def test_redact_event_v2(self):
        """
        Test redacted_events
        """
        redacted_event = redact_event(VALID_EVENT)
        self.assertEqual(
            REDACTED_EVENT,
            redacted_event,
            msg="redacted_events has incorrect order",
        )
