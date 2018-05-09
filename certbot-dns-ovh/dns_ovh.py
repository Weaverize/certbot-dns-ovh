"""Certbot OVH authenticator plugin."""
import collections
import logging
import time
import ovh

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
    ttl = 0

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
		self._client = ovh.Client()

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return "Solve a DNS01 challenge using OVH DNS"

    def _perform(self, domain, validation_domain_name, validation): # pylint: disable=missing-docstring
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
		id_record = client.post('/domain/zone/%s/record' % basedomain,
								fieldType="TXT",
								subDomain=subdomain,
								ttl=0,
								target=token)
		print (str(id_record["id"]))
		self._client.post('/domain/zone/%s/refresh' % basedomain)
		time.sleep(5)
		return id_record["id"]

	def _cleanup(self, domain, validation_domain_name, validation):
		id_record = os.environ['CERTBOT_AUTH_OUTPUT']
		client = ovh.Client()
		ndd = os.environ['CERTBOT_DOMAIN']
		ndd = ndd.split(".")
		basedomain = ndd[len(ndd)-2] + "." + ndd[len(ndd)-1]
		client.delete('/domain/zone/%s/record/%s' % (basedomain, id_record))
		client.post('/domain/zone/%s/refresh' % basedomain)