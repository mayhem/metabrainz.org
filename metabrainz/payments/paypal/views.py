from flask import Blueprint, request, current_app
from werkzeug.datastructures import ImmutableOrderedMultiDict
from metabrainz.model.payment import Payment
from itertools import chain
import requests
import logging

payments_paypal_bp = Blueprint('payments_paypal', __name__)

PAYPAL_URL_PRIMARY = 'https://www.paypal.com/cgi-bin/webscr'
PAYPAL_URL_SANDBOX = 'https://www.sandbox.paypal.com/cgi-bin/webscr'

IPN_VERIFY_EXTRA_PARAMS = ((u'cmd', u'_notify-validate'),)


@payments_paypal_bp.route('/ipn', methods=['POST'])
def ipn():
    """Endpoint that receives Instant Payment Notifications (IPNs) from PayPal.

    Options that we use are:
    0 - can contact flag
    1 - anonymous flag
    2 - is donation flag
    4 - invoice number

    Specifications are available at https://developer.paypal.com/docs/classic/ipn/integration-guide/IPNImplementation/.
    """
    request.parameter_storage_class = ImmutableOrderedMultiDict

    # Checking if data is legit
    paypal_url = PAYPAL_URL_PRIMARY if current_app.config['PAYMENT_PRODUCTION'] else PAYPAL_URL_SANDBOX
    verify_args = chain(IPN_VERIFY_EXTRA_PARAMS, request.form.items())
    verify_string = u'&'.join((u'%s=%s' % (param, value) for param, value in verify_args))
    verification_response = requests.post(paypal_url, data=verify_string.encode('utf-8'))

    # Some payment options don't return payment_status value.
    if 'payment_status' not in request.form:
        logging.warning('PayPal IPN: payment_status is missing.')
        return '', 200

    if verification_response.text == 'VERIFIED':
        Payment.process_paypal_ipn(request.form)
    else:
        logging.warning('Unverified PayPal IPN.')

    return '', 200
