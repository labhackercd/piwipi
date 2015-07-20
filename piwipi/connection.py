# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from pyexchange import ExchangeNTLMAuthConnection as BaseExchangeNTLMAuthConnection
from pyexchange.exceptions import FailedExchangeException


class ExchangeNTLMAuthConnection(BaseExchangeNTLMAuthConnection):
    """
    Wrapper around ExchangeNTMLAuthConnection that implements the `verify_certificate` flag.
    """

    def __init__(self, *args, **kwargs):
        verify_certificate = kwargs.get('verify_certificate', True)

        super(ExchangeNTLMAuthConnection, self).__init__(*args, **kwargs)

        if not hasattr(self, 'verify_certificate'):
            self.verify_certificate = verify_certificate

    def send(self, body, headers=None, retries=2, timeout=30, encoding=u"utf-8"):
        if not self.session:
            self.session = self.build_session()

        try:
            response = self.session.post(self.url, data=body, headers=headers, verify=self.verify_certificate)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise FailedExchangeException(u'Unable to connect to Exchange: %s' % err)

        return response.text
