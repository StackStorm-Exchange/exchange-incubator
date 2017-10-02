# stackstorm-napalm-logs

[napalm-logs](https://github.com/napalm-automation/napalm-logs) is an Open Source cross-vendor normalisation for network syslog messages, following the OpenConfig and IETF YANG models
maintained by napalm-automation.

## Configuration

Copy the example configuration in [napalm_logs.yaml.example](./napalm_logs.yaml.example)
to `/opt/stackstorm/configs/napalm_logs.yaml` and edit as required.

It should look like this:

```yaml
---
server_address: 1.1.1.1
server_port: 49017
auth_address: 1.1.1.1
auth_port: 49018
certificate_file: /opt/stackstorm/configs/napalm-logs.crt
```

Place your ssl certificate for the napalm-logs server in `/opt/stackstorm/configs/napalm-logs.crt` or another lcoation and update `certificate_file` in the config file.

After editing, run `sudo st2ctl reload --register-configs` to ensure your configuration
is loaded.

## Sensors
Napalm-logs registers a sensor, `napalm\_logs\_client` which runs a client that connects to the napalm-logs server. Any and all parsed logs receieved from the server will fire a `napalm_logs.log` trigger into st2 containing the payload of the log.
