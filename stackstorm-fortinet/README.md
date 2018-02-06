# Fortinet Integration Pack
This pack allows you to integrate with
[Fortinet NGFW](https://www.fortinet.com/products/next-generation-firewall.html).

Here a [demo Fortinet NGFW](https://fortigate.fortidemo.com) provided by Fortinet to try.

## Configuration
Copy the example configuration in [fortinet.yaml.example](./fortinet.yaml.example) to 
`/opt/stackstorm/configs/fortinet.yaml` and edit as required.

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
  fortinet_ip: "10.10.10.10"
  username: "admin"
  password: "admin"
```

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`


## Actions

The following actions are supported:

### Address Group:
* ``create_address_group``
* ``delete_address_group``
* ``get_address_group``
* ``update_address_group``
 
### Firewall Policy:
* ``create_firewall_policy``
* ``delete_firewall_policy``
* ``get_firewall_policy``
* ``move_firewall_policy``
* ``update_firewall_policy``
 
### Address Object:
* ``create_address_object``
* ``delete_address_object``
* ``get_address_object``
* ``update_address_object``
