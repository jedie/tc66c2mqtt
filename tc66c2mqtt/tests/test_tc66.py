from unittest import TestCase

from tc66c2mqtt.tc66 import parse_tc66_packet
from tc66c2mqtt.tests.fixtures import DECRYPTED_DATA


class Tc66TestCase(TestCase):
    def test_parse_tc66_packet(self):
        # V: 5.1609       I: 0.0199       W: 0.1026
        # Ω: 259.3        mAh: 0.0        mWh: 5.0        mAh: 0.0        mWh: 0.0
        # Temp: 27.0      D+: 2.81        D-: 2.8
        parse_tc66_packet(DECRYPTED_DATA)
