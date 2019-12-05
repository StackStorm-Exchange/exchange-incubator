import powerdns
import datetime

PDNS_API = "https://my.pdns.api.domain.tld/api/v1"
PDNS_KEY = "mysupersecretbase64key"


class PowerDNSClient(object):
    def __init__(self):
        self.api_client = powerdns.PDNSApiClient(api_endpoint=PDNS_API, api_key=PDNS_KEY)
        self.api = powerdns.PDNSEndpoint(self.api_client)

    def create_zone(self, name):
        # Creating new zone on first PowerDNS server
        serial = datetime.date.today().strftime("%Y%m%d00")
        soa = "ns0.domain.tld. admin.domain.tld. %s 28800 7200 604800 86400" % serial
        soa_r = powerdns.RRSet(
            name=name,
            rtype="SOA",
            records=[(soa, False)],
            ttl=86400
        )

        zone = self.api.servers[0].create_zone(
            name="test.python-powerdns.domain.tld.",
            kind="Native",
            rrsets=[soa_r],
            nameservers=[
                "ns1.domain.tld.",
                "ns2.domain.tld."
            ]
        )

        return zone

    def delete_zone(self, name):
        # Deleting newly created zone
        self.api.servers[0].delete_zone(name)
