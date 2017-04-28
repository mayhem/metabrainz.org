from metabrainz.testing import FlaskTestCase
from flask import url_for


class PaymentsViewsTestCase(FlaskTestCase):

    def test_donate(self):
        self.assert200(self.client.get(url_for('payments.donate')))

    def test_payment_selector(self):
        self.assert200(self.client.get(url_for('payments.payment_selector')))

    def test_payment(self):
        self.assert200(self.client.get(url_for('payments.payment', currency='usd')))
        self.assert200(self.client.get(url_for('payments.payment', currency='eur')))

    def test_cancel_recurring(self):
        self.assert200(self.client.get(url_for('payments.cancel_recurring')))

    def test_donors(self):
        response = self.client.get(url_for('payments.donors'))
        self.assert200(response)
