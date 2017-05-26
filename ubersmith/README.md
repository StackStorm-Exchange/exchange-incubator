# Ubersmith Integration Pack

This pack integrates with the subscription billing, support and device management system, Ubersmith. Allows for the creation and management of many components of Ubersmith

## Connection Configuration

You will need to specificy the details of the ubersmith instance you will be connecting to within the `/opt/stackstorm/config/ubersmith.yaml` file.
You can specificy multiple environments using nested values

```yaml
---
ubersmith:
  production:
    url: https://prod.domain.com
    api_user: apiuser
    api_token: dsfsd0f9sdf9
  dev:
    url: https://dev.domain.com
    api_user: apiuser
    api_token: d0491fkfk
```

Do not forget to run `st2ctl reload --register-configs` after you make changes to your `configs/ubersmith.yaml` file!

## Todo

## Requirements

## Actions

* `ubersmith.api_command` - Execute an Ubersmith API call

## Example

```
st2 run ubersmith.api_command ubersmith=production command=client.count
st2 run ubersmith.api_command ubersmith=production command=uber.username_exists params='{"username": "james"}'
```

## Known Bugs
