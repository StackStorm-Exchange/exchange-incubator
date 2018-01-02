# Palo Alto firewall Pack

Block threats on **Palo Alto Networks (_PAN_)** firewalls. Pack is using PAN **HTTP server profiles** (webhooks) which are available in PAN-OS version 8+
## Configuration

Copy the example configuration in **paloalto.yaml.example** to */opt/stackstorm/configs/paloalto.yaml* and edit as required.
In order to obtain *Palo Alto API key*, substitue firewall with IP address of firewall , put the username and passowrd , then run the command below.
```
curl -kgX GET 'https://firewall/api/?type=keygen&user=admin&password=password'
```

Example configuration:
```
---
  api_key: "palo_alto_api_key"
  tag: "st2"
```
## Using the pack

Configure http webhook on PAN following  [PAN-OS 8.0 documentation](https://www.paloaltonetworks.com/documentation/80/pan-os/web-interface-help/device/device-server-profiles-http)

![Snapshot of PAN webhook configuration - payload format](https://github.com/IrekRomaniuk/paloalto_blockthreats/blob/master/pan-webhook.PNG)

Name of _st2 server_ has to match st2 certificate imported to PAN. To get *st2 API key*, run the command below
 ```
st2 apikey create -k -m '{"used_by": "PAN"}'
 ```
See my blog post [here](https://medium.com/@IrekRomaniuk).

## Actions

Currently, the following actions listed below are supported:
- blockthreats

