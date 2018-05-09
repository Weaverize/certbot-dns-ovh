"""Certbot OVH authenticator plugin."""
import collections
import logging
import time
import ovh
import zope.interface

from acme import challenges

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

INSTRUCTIONS = (
    "To use certbot-dns-ovh, configure credentials as described at "
    "https://api.ovh.com/g934.first_step_with_api"
    "and add the necessary permissions for OVH access on /domain and /domain/* for all HTTP Verbs")

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """OVH Authenticator

    This authenticator solves a DNS01 challenge by uploading the answer to OVH DNS.
    """

    description = ("Obtain certificates using a DNS TXT record (if you are using OVH DNS).")
	
    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
    	self.client = ovh.Client()

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=60)

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return "Solve a DNS01 challenge using OVH DNS"

    def get_chall_pref(self, unused_domain):  # pylint: disable=missing-docstring,no-self-use
        return [challenges.DNS01]

    def _setup_credentials(self):
		pass

    def _perform(self, domain, validation_domain_name, validation): # pylint: disable=missing-docstring
        """
        Performs a dns-01 challenge by creating a DNS TXT record.

        :param str domain: The domain being validated.
        :param str validation_domain_name: The validation record domain name.
        :param str validation: The validation record content.
        :raises errors.PluginError: If the challenge cannot be performed
        """
    	ndd = domain
        token = "\"" +  validation + "\""

        ndd = ndd.split(".")
        basedomain = ndd[len(ndd)-2] + "." + ndd[len(ndd)-1]
        subdomain = "_acme-challenge"
        if len(ndd) > 2:
            subdomain += "."
            for i in range(0, len(ndd)-2):
                if i == len(ndd)-3:
                    subdomain += ndd[i]
                else:
                    subdomain += ndd[i] + "."
        self.id_record = self.client.post('/domain/zone/%s/record' % basedomain,
                                fieldType="TXT",
                                subDomain=subdomain,
                                ttl=0,
                                target=token)
        print (str(self.id_record["id"]))
        self.client.post('/domain/zone/%s/refresh' % basedomain)
        time.sleep(5)
        return self.id_record["id"]

    def _cleanup(self, domain, validation_domain_name, validation):
        """
        Deletes the DNS TXT record which would have been created by `_perform_achall`.

        Fails gracefully if no such record exists.

        :param str domain: The domain being validated.
        :param str validation_domain_name: The validation record domain name.
        :param str validation: The validation record content.
        """
    	print(str(validation))
        #id_record = os.environ['CERTBOT_AUTH_OUTPUT']
        ndd = domain
        ndd = ndd.split(".")
        basedomain = ndd[len(ndd)-2] + "." + ndd[len(ndd)-1]
        self.client.delete('/domain/zone/%s/record/%s' % (basedomain, self.id_record))
        self.client.post('/domain/zone/%s/refresh' % basedomain)