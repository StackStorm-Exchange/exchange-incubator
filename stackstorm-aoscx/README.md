# AOS-CX StackStorm Integration Pack

This StackStorm pack includes integration with the AOS-CX switching platform 
as well as workflows including third-party tools such as Ansible.

## Requirements

* Ubuntu 18.04
* Python 3.5+
* st2 3.2.0
* Minimum supported AOS-CX firmware version 10.05
* Enable REST on your AOS-CX device with the following commands:
    ```
    switch(config)# https-server rest access-mode read-write
    switch(config)# https-server vrf mgmt
    ```

## Installation

To install this pack into your local StackStorm server clone our Github repository, 
change into the downloaded directory, and install the pack using the `st2 install` command 
specifying Python3:
```
git clone https://github.com/aruba/stackstorm-aoscx.git
cd stackstorm-aoscx
st2 pack install file://$PWD --python3
```

We are currently pending review to include our pack in [StackStorm Exchange](https://exchange.stackstorm.org/). 

## Configuration
The `aoscx.yaml.example` files is an example configuration file used by the AOS-CX Websocket `port_sensor`.  
This is where you define the AOS-CX device, it's credentials, and the interfaces you want to monitor.  
Copy this to `/opt/stackstorm/configs/aoscx.yaml`.
  
## Credentials Configuration
The pack uses [REST-API](https://developer.arubanetworks.com/aruba-aoscx/docs/getting-started-with-aos-cx-rest) 
to connect to the AOS-CX switch. The following format is used to specify the credentials 
for the device. Each credential must have a username and password that is authorized for REST-API 
commands:
```yaml
credentials:
  admin:
    username: admin
    password: admin
```  

## Device Configuration
The device configuration requires the IP address of the AOS-CX device, it's credentials, 
and the list of interfaces to monitor. It is optional to provide PROXY information 
 to use in connecting to the AOS-CX Websocket. 
```yaml
device:
  ip_address: 10.100.206.188
  hostname: 8320-CX-188
  credentials: admin
  interface:
    - 1/1/1
    - 1/1/23
    - 1/1/14
  proxy:
    http: None
    https: None
```  

## Actions
Actions in this pack use REST-API to connect to the AOS-CX switch as well as third-party 
frameworks: 
- **get_link_status**: Get the link status of all interfaces on an AOS-CX switch with the specified IP address.  
- **get_aoscx_interface_tower_info**: Get MAC address and IP address of a newly connected 
device using AOS-CX and validate device needs to be provisioned using Ansible Tower API.  

## Action Workflows
Action Workflows in this pack use REST-API to connect to the AOS-CX switch as well as third-party 
frameworks: 
- **ztp_ansible_tower_workflow**: A workflow that runs an Ansible Tower Job Template 
after retrieving device LLDP information on an AOS-CX switch.  

## Sensors
There is one Sensor currently implemented in this pack:
 - **aoscx.PortSensor**: Sensor that monitors the admin status of AOS-CX switch's interfaces.  
  
## Rules and Triggers
This pack defines rules for handling syslog or websocket events from AOS-CX devices:  
- **port_sensor_rule**: Using the AOS-CX Websocket PortSensor, retrieves the admin status of all interfaces on an AOS-CX switch when an interface goes down.  
- **ztp_ansible_tower_workflow_rule**: Starts the ztp_ansible_tower_worfklow when an interface link on AOS-CX comes up via Syslog message.


## Contribution
At Aruba Networks we're dedicated to ensuring the quality of our products, so if you find any
issues at all please open an issue on our [Github](https://github.com/aruba/stackstorm-aoscx) and we'll be sure to respond promptly!

For more contribution opportunities follow our guidelines outlined in our [CONTRIBUTING.md](https://github.com/aruba/stackstorm-aoscx/blob/master/CONTRIBUTING.md)