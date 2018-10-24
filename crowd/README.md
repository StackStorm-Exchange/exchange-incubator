
# Crowd Integration Pack

Pack for integration of Crowd into StackStorm. The pack includes the
functionality to perform actions on Crowd through StackStorm.

## Configuration

Copy the example configuration in [crowd.yaml.example](./crowd.yaml.example)
to `/opt/stackstorm/configs/crowd.yaml` and edit as required.

It must contain:

* ``app_url`` - URL for the Crowd application 
* ``app_user`` - Crowd application user
* ``app_pass`` - Crowd application password

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Actions

