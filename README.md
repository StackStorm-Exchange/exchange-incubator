# menandmice Integration Pack

## Configuration
TODO: Describe configuration


# Sensors

## Example Sensor
TODO: Describe sensor


# Actions

## example


``` shell
$ st2 run menandmice.add_dns_records server=menandmice.domain.tld username=administrator password=xxx dns_records='{"dnsRecord": [ {"name": "testserver.domain.tld.", "type": "A", "data": "10.1.2.100", "enabled": true, "dnsZoneRef": "{#1-#234}" } ] }'
..
id: 59556158a814c03b10b9999
status: succeeded
parameters: 
  dns_records:
    dnsRecord:
    - data: 10.1.2.100
      dnsZoneRef: '{#1-#234}'
      enabled: true
      name: testserver.domain.tld.
      type: A
  password: '********'
  server: menandmice.domain.tld
  username: administrator
result: 
  exit_code: 0
  result:
    errors: null
    objRefs:
      ref:
      - '{#11-#1271}'
  stderr: ''
  stdout: ''

```

``` shell
$ st2 run menandmice.get_dns_zones server=menandmice.domain.tld username=administrator password=xxx filter="type: Master"

.................
id: 59555e63a814c0698925a1aa
status: succeeded
parameters: 
  filter: 'type: Master'
  password: '********'
  server: menandmice.domain.tld
  username: administrator
result: 
  exit_code: 0
  result:
    dnsZones:
      dnsZone:
      - adIntegrated: true
        adPartition: null
        adReplicationType: null
        authority: '[Active Directory - domain.tld]'
        customProperties: null
        dnsScopeName: null
        dnsViewRef: null
        dnsViewRefs:
          ref:
          - '{#2-#1}'
          - '{#2-#2}'
        dnssecSigned: false
        dynamic: true
        kskIDs: null
        name: 2.1.10.in-addr.arpa.
        ref: '{#1-#234}'
        type: Master
        zskIDs: null
    totalResults: 1
  stderr: ''
  stdout: ''
```
