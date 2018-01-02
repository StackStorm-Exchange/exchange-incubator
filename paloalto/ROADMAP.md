## Roadmap:

##### Add actions:
- unblock ip (or deregister from DAG)

## TO DO

##### Add 'trusted' parameter:
Add either action or config parameter to exclude sources blocked i.e. rfc1918 addresses
trusted: '10.0.0.0/8'
from netaddr import IPNetwork, IPAddress
if IPAddress("192.168.0.1") in IPNetwork("192.168.0.0/24"):
    print "Yay!"

##### Criteria to exclude threat types
ThreatContentName, Severity, Action i.e. only Critical and Alert

##### Add to action:
self.logger.info('Action successfully completed')
self.logger.error('Action failed...')

