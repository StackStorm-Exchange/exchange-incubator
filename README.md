[![Build Status](https://circleci.com/gh/EncoreTechnologies/stackstorm-menandmice.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/EncoreTechnologies/stackstorm-menandmice) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Men&Mice Integration Pack

# <a name="Introduction"></a> Introduction

This pack provides integration with the Men&Mice IPAM [SOAP API](http://api.menandmice.com/8.2.0/).
Actions within this pack mirror one-for-one the "Commands" in the SOAP API.
Data types and payloads also mirror one-for-one.


# <a name="QuickStart"></a> Quick Start

1. Install the pack

    ``` shell
    st2 pack install menandmice
    ```
    
2. Execute an action (example: list all DNS Zones)

    ``` shell
    st2 run menandmice.get_dns_zones server=menandmice.domain.tld username=administrator password=xxx
    ```

# <a name="Configuration"></a> Configuration

The configuration for this pack is used to specify connection information for
all Men&Mice servers you'll be communicating with. The location for the config file
is `/opt/stackstorm/config/menandmice.yaml`.


**Note** : `st2 pack config` doesn't handle schemas refernences very well (known bug)
    so it's best to create the configuraiton file yourself and copy it into
    `/opt/stackstorm/configs/menandmice.yaml` then run `st2ctl reload --register-configs`
    
## <a name="Schema"></a> Schema

``` yaml
---
menandmice:
  <connection-name-1>:
    server: <hostname or ip of the Men&Mice server>
    username: <username@domain.tld (preferred) or domain\username>
    password: <password for username>
  <connection-name-2>:
    server: <hostname or ip of the Men&Mice server>
    username: <username@domain.tld (preferred) or domain\username>
    password: <password for username>
    port: <port number override to use for the connections: default = None (defaults to 80/443)>
    transport: <transport override to use for the connections: default = http'>
    wsdl_endpoint: <HTTP URL for the M&M WSDL: default = '_mmwebext/mmwebext.dll?wsdl'>
  <connection-name-3>:
    ... # note: multiple connections can be specified!
```

## <a name="SchemaExample"></a> Schema Examples

``` yaml
---
menandmice:
  dev:
    server: menandmice.dev.domain.tld
    username: stackstorm_svc@dev.domain.tld
    password: DevPassword
  stage:
    server: menandmice.stage.domain.tld
    username: stackstorm_svc@stage.domain.tld
    password: stagePassword
    port: 8080
  prod:
    server: menandmice.prod.domain.tld
    username: stackstorm_svc@prod.domain.tld
    password: SuperSecret
    transport: https
```

**Note** : All actions allow you to specify a `connection` name parameter that will
           reference the conneciton information in the config. Alternatively
           all actions allow you to override these connection parameters
           so a config isn't required. See the [Actions](#Actions) for more
           information.

# Actions

Actions in this pack are auto-generated from the Men&Mice IPAM 
[SOAP API](http://api.menandmice.com/8.2.0/) operations defined in the WSDL file
(note: we store these WSDLs in the `etc/` directory of this pack). There is
an action created for every "Command" in the Men&Mice API. Input and output
parameters should be the same with all action names and action parameters
convert from CamelCase to snake_case. Example: SOAP command [AddDNSServer](http://api.menandmice.com/8.1.0/#AddDNSServer)
will be converted to snake_case for the action to become `menandmice.add_dns_server`.
In this same command one of the arguments is `dnsServer` that becomes the 
`dns_server` action parameter.


## <a name="UsageBasic"></a> Usage - Basic

The following example demonstrates running the `menandmice.get_dns_zones` action
using connection information specified as action input parameters.

``` shell
$ st2 run menandmice.get_dns_zones server=menandmice.domain.tld username=administrator password=xxx
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

The basic example is great and allows for quick testing from the commandline and/or
one-off commands in a workflow. However, specifying the same connection information
over/over can become tedious and repetitive, luckyily there is a better way.


## <a name="UsageConfig"></a> Usage - Config Connection

This pack is designed to store commonly used connection information in the pack's
config file located in `/opt/stackstorm/config/menandmice.yaml`. The connection 
info is specified in the config once, and then referenced by name within an
action and/or workflow. 

Using the action from the basic example, we can enter this connection information
in our config:

``` shell
$ cat /opt/stackstorm/configs/menandmice.yaml
---
menandmice:
  prod:
    server: menandmice.domain.tld
    username: administrator
    password: xxx
```

Now we can reference this connection (by name) when executing our action:

``` shell
$ st2 run menandmice.get_dns_zones connection=prod
...
```

This pays off big time when running multiple commands in sequence.


## <a name="UsageLogin"></a> Usage - Login Sessions

By default this pack performs a login operation in every action if the `session` 
parameter is not passed in. To avoid these repetitive logins under the hood
we can perform the login operation and then re-use the login session cookie
in all subsequent actions within a workflow. 

**Note**: When using a cached login session you still need to pass in a `server`
          parameter either as an action parameter or as part of the `connection`.
          Without the `server` we can't build the WSDL URL necessary to establish
          a SOAP connection to the server.

``` yaml
version: '2.0'

menandmice.wf_login_sessions:
  description: 
  input:
    - connection
    - server
    - username
    - password
    - port
    - transport
  output:
    - dns_servers
    - master_dns_zones
  tasks:
    main:
      action: std.noop
      on-success:
        - login
        - get_dns_servers
        - get_dns_zones
        
    login:
      action: menandmice.login
      input:
        connection: "{{ _.connection }}"
        server: "{{ _.server }}"
        username: "{{ _.username }}"
        password: "{{ _.password }}"
        port: "{{ _.port }}"
        transport: "{{ _.transport }}"
      publish:
        session: "{{ task('login').result.result.session }}"
      on-error:
        fail
    
    get_dns_servers:
      workflow: menandmice.get_dns_servers
      input:
        session: "{{ _.session }}"
        server: "{{ _.server }}"
      publish:
        dns_servers: "{{ task('get_dns_servers').result.result.dnsServers.dnsServer }}"

    get_dns_zones:
      workflow: menandmice.get_dns_servers
      input:
        session: "{{ _.session }}"
        server: "{{ _.server }}"
        filter: "type:Master"
      publish:
        master_dns_zones: "{{ task('get_dns_zones').result.result.dnsZones.dnsZone }}"
```

For an even more extensive example see `actions/workflows/wf_add_dns_zone.yaml`


## <a name="UsageObjects"></a> Usage - Complex Object Types

Many of the actions in the SOAP API take a complex object type as an input parameter.
For example we're going to look at the SOAP command [AddDNSRecords](http://api.menandmice.com/8.1.0/#AddDNSRecords)
that maps to the action `menandmice.add_dns_records`. This command takes an argument
`dnsRecords` with a datatype of [`ArrayOfDNSRecord`](http://api.menandmice.com/8.1.0/#ArrayOfDNSRecord).
To facilitate this all command arguments that take complex object types map
to action arguments of type `object`. This means that the data passed into this
parameter can be a python `dict` or `list`, making it work like a native datastructure
within workflows. Also, on the commandline using `st2 run` we an specify these
type of objects using a JSON string that will then be auto-converted into 
a python `dict` or `list` when the commandline argument is parsed.

Navigating the SOAP documentation can be a little cumbersome, so to help users
out we've insert the expected object structure in the description
for these complext data type parameters. These object structures are described
in JSON format for easy reading and understandability. We hope this helps!

In the example below you can see both how the JSON string input works for
`st2 run` along with what the datastructure looks like as an input parameter.

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

For another example see `actions/workflows/wf_add_dns_zone.yaml`. The `build_master_zone:`
task creates a `DNSZone` object and publishes it to the `master_zone` variable. 
Then in the `add_master_zone:` task we pass the `DNSZone` object `master_zone`
into the `dns_zone` parameter for the `menandmice.add_dns_zone` action.

# Version Compatiblity

| Pack Version | Men&Mice Version | WSDL File |
|--------------|------------------|-----------|
| 0.1.0        | 8.1.0            | `etc/menandmice_wsdl_2017_06_26.xml` |

# TODO
- Update etc/README.md on how to generate code

# Future
- Create sensors to trigger events on changes (look at the the GetHistory command)
