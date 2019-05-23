# NSOne

This pack enables the integration of NSOne into Stackstorm

# Configuration

To create and install the config file, you can run:

`st2 pack config nsone`

Alternatively, you can copy the example configuration in
[nsone.yaml.example](./nsone.yaml.example)
to `/opt/stackstorm/configs/nsone.yaml` and edit as required.

* `api_key:` API-KEY
* `debug:` optional debug flag. Set to True for additional logging

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Creating API Key in NSOne

* Sign into NSOne
* Go to 'Account Settings' > 'API Keys'
* Click on 'Add Key' and select the permissions this API should have.
* Add the API Key to the Pack's config.

## Configuration

```yaml
---
api_key: abcd1234ABCD
debug: false
```

# Actions

## Account

* `account.get` - Get data about your account

## Feeds

* `feed.create` - Create a feed in a data source
* `feed.delete` - Delete a feed in a data source
* `feed.get` - Get details about a feed in a data source
* `feed.list` - List all feeds in a data source
* `feed.update` - Update a feed in a data source

## Monitors

* `monitor.get` - Get details about a monitor
* `monitor.list` - List all monitors

## Notify List

* `notify_list.get` - Get details about a notification list
* `notify_list.list` - List all notification lists

## Records

* `record.create` - Create a record
* `record.delete` - Delete a record
* `record.get` - Get details about a record
* `record.update` - Update a record

## Data Sources

* `source.create` - Create a data source
* `source.delete` - Delete a data source
* `source.get` - Get details about a data source
* `source.list` - List all data sources
* `source.publish` - Publish a data source
* `source.update` - Update a data source

## Stats

* `stats.qps` - Get QPS (Queries per second) details about your Account, a Zone, or a Record
* `stats.usage` - Get usage details about your Account, a Zone, or a Record

## Zones

* `zone.create` - Create a zone
* `zone.delete` - Delete a zone
* `zone.get` - Get details about a zone
* `zone.list` - List all zones
* `zone.search` - Search a zone for records
* `zone.update` - Update a zone

# References

* NS1 API Reference - https://ns1.com/api
* `ns1-python` Reference - https://ns1-python.readthedocs.io/en/latest/index.html
* `ns1-python` Source - https://github.com/ns1/ns1-python
  - This is the SDK Being used by this pack
  - Currently this pack's logic leverages the Modules found in `ns1-python/ns1/rest`

# Future

* Actions covered by methods in `ns1-python/ns1/rest/ipam.py`
* Actions for `monitor.create`, `monitor.update`, `monitor.delete` in `ns1-python/ns1/rest/monitoring.py`
* Actions for `notify_list.create`, `notify_list.update`, `notify_list.delete` in `ns1-python/ns1/rest/monitoring.py`
