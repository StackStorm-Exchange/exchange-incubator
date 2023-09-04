# withitems Integration Pack

StackStorm integration pack for faster `with-items` in orquesta workflows

## Quick Start

Run the following commands to install this pack and the install  on your StackStorm host:

``` shell
st2 pack install withitems
st2 pack configure withitems
```

## Configuration

Copy the example configuration in [withitems.example.yaml](./withitems.example.yaml)
to `/opt/stackstorm/configs/withitems.yaml` and edit as required.

* `st2api_key`- optional key for preventing token timeouts
* `st2apiurl` - url for api
* `st2authurl` - url for authentication
* `st2baseurl` - url for base stackstorm api

### Configuration Example

The configuration below is an example of what a end-user config might look like.
``` yaml
st2api_key: null
st2apiurl: https://localhost:443/api
st2authurl: https://localhost:443/auth
st2baseurl: https://localhost:443
```

## Actions

* `withitems.with_items`


### Action workflow Example - withitems.with_items
with_items will be used inside a workflow.  Here is an example of that. The YAQL select function is very handy to format a list of objects to pass as a parameter.
``` shell
---    
    version: 1.0 
    
    description: A with items example
    
    input:
      - list_items
    
    tasks:
      task1:
        action: withitems.with_items
        input:
          action: core.echo
          parameters: "<% ctx().list_items.select({\"message\"=>concat(\"message \", $)}) %>"
        next:
          - when: <% succeeded() %>
            do: task2
      task2:
        action: core.noop
```
