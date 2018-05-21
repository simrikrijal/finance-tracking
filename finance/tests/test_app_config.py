from django.test import TestCase

from ..apps import FinanceTrackingConfig


class AppConfigTest(TestCase):
    def test(self):
        self.assertEqual(FinanceTrackingConfig.name, 'finance')
