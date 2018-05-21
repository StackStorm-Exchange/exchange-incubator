# xcontrol Integration Pack

## Configuration
Copy the example configuration in [xcontrol.yaml.example](./xcontrol.yaml.example) to 
`/opt/stackstorm/configs/xcontrol.yaml` and edit as required.

It must contain:

```
xcontrol_ip - Your xcontrol IP address
username - xcontrol Username
password - xcontrol Password
```

You can also use dynamic values from the datastore. See the 
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

Example configuration:

```yaml
---
  xcontrol_ip: "10.10.10.10"
  username: "root"
  password: "extreme"
```

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`


## Actions

The following actions are supported:
* ``add_mac_to_blacklist``
* ``remove_mac_from_blacklist``
* ``get_endsystem_mac_from_ip``

## Workflow:

The following Workflow are supported:
* ``remove_vm_from_blacklist_wf``
* ``add_vm_to_blacklist_wf``