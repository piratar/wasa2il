from base64 import b64decode
from datetime import datetime
from signxml import XMLVerifier
from xml.etree import ElementTree

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class SamlException(Exception):
    pass


def authenticate(request, redirect_url):
    token = request.POST.get('token')

    if not token:
        return HttpResponseRedirect(redirect_url)

    # XML is received as a base64-encoded string.
    input_xml = b64decode(token)

    # Fetch the certificate from within the XML (enveloped).
    cert = ElementTree.fromstring(input_xml).find('.//{http://www.w3.org/2000/09/xmldsig#}X509Certificate').text

    # Check signature and retrieve the XML that's guaranteed to be signed.
    signed_xml = XMLVerifier().verify(input_xml, x509_cert=cert).signed_xml

    # Respect expiry boundaries given in SAML.
    # Apparently the datetimes have 7 digits of microseconds when normally
    # they should be 6 when parsed. We'll leave them out by only using the
    # first 19 characters.
    conds_xml = signed_xml.find('.//{urn:oasis:names:tc:SAML:2.0:assertion}Conditions')
    time_limit_lower = datetime.strptime(conds_xml.attrib['NotBefore'][:19],'%Y-%m-%dT%H:%M:%S')
    time_limit_upper = datetime.strptime(conds_xml.attrib['NotOnOrAfter'][:19],'%Y-%m-%dT%H:%M:%S')
    now = datetime.now()
    if time_limit_lower > now or time_limit_upper < now:
        raise SamlException('Remote authentication expired')

    # Find the assertion ID for our records. This is not needed for
    # functionality's sake and is only kept for the hypothetical scenario
    # where a particular authentication needs to be matched with records on
    # the identity provider's side.
    assertion_id = signed_xml.find('.//{urn:oasis:names:tc:SAML:2.0:assertion}Assertion').attrib['ID']

    # Translate SAML attributes into a handy dictionary.
    attributes = {}
    for attribute in signed_xml.findall('.//{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
        attributes[attribute.attrib['Name']] = attribute.find('.//{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue').text

    # Get data from SAML attributes.
    name = attributes['Name']
    ssn = attributes['UserSSN']

    return { 'ssn': ssn, 'name': name, 'assertion_id': assertion_id }
