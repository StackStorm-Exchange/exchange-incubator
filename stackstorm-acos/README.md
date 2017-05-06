# ACOS Integration Pack
This pack integrates the ACOS-based appliance of A10 Networks which support aXAPI v2.1 or v3.0.

## Configuration
You will need to specify a set of following credentials to connect.

```yaml
appliance:
  target: # IP address or hostname of appliance to connect
  userid:
  passwd:
```

## Actions
| params                        | description                                                     |
|:------------------------------|:----------------------------------------------------------------|
| add_slb_server                | register a server to the SLB                                    |
| add_slb_service_group_member  | add a server to the ServiceGroup as a member                    |
| add_slb_service_group         | register a ServiceGroup to the SLB                              |
| add_slb_virtual_server        | Add a VirtualServer to SLB                                      |
| del_slb_server                | remove a server which is registered in SLB                      |
| del_slb_service_group_member  | remove a server to the ServiceGroup as a member                 |
| del_slb_service_group         | remove a ServiceGroup from SLB                                  |
| del_slb_virtual_server        | remove a VirutlServer from SLB                                  |
| get_slb_server                | get a Server information which is registered in SLB             |
| get_slb_service_group_members | get members information which are belonged to the ServiceGroup  |
| get_slb_service_group         | get a ServiceGroup information which is registered in SLB       |
| get_slb_virtual_server        | get VirtualServer which is registered in the SLB                |
| list_slb_servers              | lists servers which are registered in SLB                       |
| list_slb_service_groups       | lists ServiceGroup entries which are registered in SLB          |
| list_slb_virtual_servers      | list VirtualServers which are registered in the SLB             |
