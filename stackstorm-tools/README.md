# Tools Pack

## Actions

### `download`
### `archive.extract`
### `relay`

```
route_action:
    action: tools.relay
    input:
        objects:
            foo: <% $.foo %>
            bar: <% $.bar %>
    publish:
        foo: <% task(route_action).result.result.foo %>
        bar: <% task(route_action).result.result.bar %>
    on-success:
        - action1: <% condition %>
        - action2: <% condition %>
        - action3: <% condition %>
```


