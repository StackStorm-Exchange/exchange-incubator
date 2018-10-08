# Nginx Plus Integration Pack

This pack provides an integration between StackStorm and [Nginx Plus](https://www.nginx.com/products/nginx/).
The actions in this pack implement [Nginx Plus REST API](http://nginx.org/en/docs/http/ngx_http_api_module.html).

## <a name="quickstart"></a> Quick Start

**Steps**

1. Install the pack

    ``` shell
    st2 pack install nginxplus
    ```

2. Run an action to list nginx stats

    ``` shell
    $ st2 run nginxplus.nginx.get server=ngx.example.com
    .
    id: 5bbbb56d2db7aa7f4abcedd1
    status: succeeded
    parameters: 
      server: ngx.example.com
    result: 
      body:
        address: 10.10.16.4
        build: nginx-plus-r16
        generation: 25
        load_timestamp: '2018-10-08T19:24:32.456Z'
        pid: 21838
        ppid: 1934
        timestamp: '2018-10-08T19:52:13.942Z'
        version: 1.15.2
      headers:
        Cache-Control: no-cache
        Connection: keep-alive
        Content-Length: '194'
        Content-Type: application/json
        Date: Mon, 08 Oct 2018 19:52:13 GMT
        Expires: Thu, 01 Jan 1970 00:00:01 GMT
        Server: nginx/1.15.2
      parsed: true
      status_code: 200

    ```

## <a name="configuration"></a> Configuration

This pack does not require a configuration file. All connection parameters must be passed
into each action individually. A configuration file to store connection information
may be added in a future release.

## <a name="actions"></a> Actions

Actions in this pack are based on the [Nginx Plus REST API](http://nginx.org/en/docs/http/ngx_http_api_module.html).

| Action | Description |
|--------|-------------|
| nginxplus.connections.delete | Reset client connections statistics |
| nginxplus.connections.get | Get client connections statistics |
| nginxplus.http.caches.delete | Reset cache statistics |
| nginxplus.http.caches.get | Get status of all or specific cache(s) |
| nginxplus.http.get | Get list of HTTP-related endpoints |
| nginxplus.http.keyvals.delete | Empty the HTTP keyval zone |
| nginxplus.http.keyvals.get | Get key-value pairs from all or specific HTTP keyval zone(s) |
| nginxplus.http.keyvals.patch | Modify a key-value or delete a key |
| nginxplus.http.keyvals.post | Add a key-value pair to the HTTP keyval zone |
| nginxplus.http.requests.delete | Reset HTTP requests statistics |
| nginxplus.http.requests.get | Get HTTP requests statistics |
| nginxplus.http.server_zones.delete | Reset statistics for an HTTP server zone |
| nginxplus.http.server_zones.get | Get status of all or specific HTTP server zone(s) |
| nginxplus.http.upstreams.delete | Reset statistics of an HTTP upstream server group |
| nginxplus.http.upstreams.get | Get status of all or specific HTTP upstream(s) |
| nginxplus.http.upstreams.servers.delete | Remove a server from an HTTP upstream server group |
| nginxplus.http.upstreams.servers.get | Get all servers from http upstream |
| nginxplus.http.upstreams.servers.patch | Patch backend servers for http upstream |
| nginxplus.http.upstreams.servers.post | Add a server to an HTTP upstream server group |
| nginxplus.nginx.get | Get status of nginx running instance |
| nginxplus.processes.delete | Reset nginx processes statistics |
| nginxplus.processes.get | Get nginx processes status |
| nginxplus.slabs.delete | Reset slab statistics |
| nginxplus.slabs.get | Get status of all or specific slab(s) |
| nginxplus.ssl.delete | Reset SSL statistics |
| nginxplus.ssl.get | Get SSL statistics |
| nginxplus.stream.get | Get list of stream-related endpoints |
| nginxplus.stream.keyvals.delete | Empty the stream keyval zone |
| nginxplus.stream.keyvals.get | Get key-value pairs from all or specific stream keyval zone(s)|
| nginxplus.stream.keyvals.patch | Modify a key-value or delete a key |
| nginxplus.stream.keyvals.post | Add a key-value pair to the stream keyval zone |
| nginxplus.stream.server_zones.delete | Reset statistics for a stream server zone |
| nginxplus.stream.server_zones.get | Get status of all stream server zones |
| nginxplus.stream.upstreams.delete | Reset statistics of a stream upstream server group |
| nginxplus.stream.upstreams.get | Get status of all stream upstream server groups |
| nginxplus.stream.upstreams.servers.delete | Remove a server from a stream upstream server group |
| nginxplus.stream.upstreams.servers.get | Get configuration of all or specific server(s) in a stream upstream server group |
| nginxplus.stream.upstreams.servers.patch | Modify a server in a stream upstream server group |
| nginxplus.stream.upstreams.servers.post | Add a server to a stream upstream server group |
| nginxplus.stream.zone_sync.get | Get sync status of a node |

