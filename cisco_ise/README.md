# Integration Pack for Cisco ISE

## cisco_ise

This pack uses [requests](https://requests.readthedocs.io/en/master/) to send and receive data from the ISE API

# Quick-Start

1. Install the pack: `st2 pack install cisco_ise`
2. Ensure ISE and [ERS is set up](https://developer.cisco.com/docs/identity-services-engine/#!setting-up) for API usage
3. Run the action `internal_user.get_all` and confirm you received a list of 'Internal Users'

# Configuration

To create and install the configuration file, run:

`st2 pack config cisco_ise`

Alternatively, you can copy the example configuration in
[cisco_ise.yaml.example](./cisco_ise.yaml.example)
to `/opt/stackstorm/configs/cisco_ise.yaml` and edit as required.

`connections` is a parent key containing a dictionary of connections that can be referenced by name to use as the connection parameters for action. (Big thanks to the team at Encore Technologies for being my reference material on this aspect of the pack)

Each connection should be a dictionary with one or more of the following keys.

##### Example:

```yaml
---
connections:
  ise_prod:
    hostname: <host.domain.com>
    api_user: <value>
    api_pass: <value>
```

You can then reference the name of the key in the `connection_name` parameter of the action to load that connection.

Alternatively, you can pass any of the relevant fields directly to the action at run time.

When conflicting values are provided (specifying `connection_name` as well as a `hostname` in the action), the pack will resolve the conflict by using Action values to override the values imported from the config by `connection_name` (Pack determined logic)

For example, if you supply a User/Pass in the configuration, reference it in the action, and a hostname in the action fields directly, you will connect to the host supplied directly to the Action at run time, using the credentials from the pack config.

This behavior is the same for any connection related parameter such as verify_ssl and use_http.

The `hostname` field should contain only an FQDN. Do not include protocol (`https://`), Ports (`:8090`), or paths (`/ers/config`). This info is added to the hostname in [base.py](/actions/lib/base.py).

##### Recommendations

You can also use dynamic values from the datastore for sensitive information. See the [docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

An example of this is provided in [the example config](./cisco_ise.yaml.example).
You can set this value with `st2 key set '<key name>' '<value>' --encrypt` and reference in your config with `"{{ st2kv.system.<key name> | decrypt_kv }}"`

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please remember to tell StackStorm to load these new values by running `st2ctl reload --register-configs`

# Pack Design

## Action Naming

`uri_resource_name.operation`

Actions are named somewhat consistently with how they are presented in the official documentation. This is in an attempt to create a clear correlation between official documentation and pack actions. Some slight modifications were made to reduce action name length.

##### Example:

In the ISE documentation, there is a resource for [`internaluser`](https://developer.cisco.com/docs/identity-services-engine/#!internal-user) and operation of [Get-By-Id](https://developer.cisco.com/docs/identity-services-engine/#!internal-user/get-by-id). By sending an HTTP `GET` to `/ers/config/internaluser/{id}` you can retrieve a user by id.

The corresponding action in this pack is named [`internal_user.get_by_id`](./actions/internaluser.get_by_id.yaml)

## Code Structure

Why was the [ISE python package](https://pypi.org/project/ISE/) not used?

There is a PIP Package for ISE that was originally developed by [bobthebutcher](https://github.com/bobthebutcher) and [mpenning](https://github.com/mpenning) for ISE `2.0`.
This package was updated by [falkowich](https://github.com/falkowich) and [karrots](https://github.com/karrots) for ISE `2.4` and notes that testing for `2.7.0` has been completed.

The history of this pack is a great example of the power of OSS, and there is no question about the capability or quality of this package. The reason it was not selected was:

ISE leverages native HTTP Methods and a (somewhat) consistent URI structure.

Writing a simple API client allows for actions to be defined in YAML only, without the need for special usage on a per action basis. Using the Python ISE Package requires new features and capabilities to be added to the python package and the creation of new python actions for this pack. Adding new features via YAML actions is quicker and easier. Alternatively, as a stop-gap, the [request.raw](./actions/request.raw) action allows transparent use of the action logic if there is not a change to the pack. That supports the use of new features before a pack update.

* [base.py](./actions/lib/base.py) - Contains all the shared logic used by every python action
  * Contains multiple methods intended for use in different ways. Any method not intended to be used directly is prefixed with a single underscore so it isn't imported with `from lib.base import BaseAction`
* [action.py](./actions/action.py) - The default action that calls the necessary class methods to execute an action.
  * Uses the methods `action_setup()` and `api_client()` to prepare and parse data and handle the resulting response from the `api_request()` method. (Paging for example)
* [raw_action.py](./actions/raw_action.py) - An action that only leverages the `retieve_config_connection()`, `api_request()`, and `format_action_result()` methods.
  * This action allows for some future-proofing as well as showing alternative ways to use the methods of this pack in a case where customized action logic is required.

# References

##### Cisco ISE

* [Official ISE Documentation](https://www.cisco.com/c/en/us/support/security/identity-services-engine/series.html)
* [Official ISE API Documentation](https://developer.cisco.com/docs/identity-services-engine/#!cisco-ise-api-documentation)

##### Requests for Python
* [Requests](https://requests.readthedocs.io/en/master/)

# Future

* Unit Testing
* Logic to understand unique payload structure for each action, allowing field-based inputs rather than JSON Object input for payload.
