# CheckPoint Integration Pack

## Configuration
Copy the example configuration in [checkpoint.yaml.example](./checkpoint.yaml.example) to 
`/opt/stackstorm/configs/checkpoint.yaml` and edit as required.

It must contain:

```
firewall_ip - Your fortigate appliance IP address
username - Firewall Username
password - Firewall Password
```

You can also use dynamic values from the datastore. See the 
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

Example configuration:

```yaml
---
  checkpoint_ip: "10.10.10.10"
  username: "admin"
  password: "admin"
```

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`


## Actions

The following actions are supported:

### Firewall Policy:
* ``create_checkpoint_policy``
* ``delete_checkpoint_policy``
