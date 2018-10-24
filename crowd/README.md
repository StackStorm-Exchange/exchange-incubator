
# Crowd Integration Pack

Pack for integration of [Crowd](https://developer.atlassian.com/server/crowd/crowd-rest-apis/) into StackStorm. The pack includes the
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

* `check_user` - Action to check if the user already exists in Crowd.
* `get_user` - Action to get given user details from Crowd.
* `add_user` - Action to add a user to the directory. 
* `set_active` - Action to set/change the active state of a user.
* `set_user_attribute` - Action to set/change an attribute on a existing user.
* `add_user_to_group` - Action to add a user to a group.
* `get_groups` - Action to retrieves a list of group names that have given user as a direct member.

