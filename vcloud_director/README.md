# VCloud Director

## Description
Basic actiosn to integrate with VCloud Director.


## Connection Configuration
Copy the sample configuration file [vcloud_director.yaml.example] to `/opt/stackstorm/configs/vcloud_director.yaml` and edit as required.
Required fields for connecting to vcloud are address, user and password.


## Actions
* `vcloud_director.get_org` - Retrieve a single organisation details
* `vcloud_director.get_orgs` - Retrieve a list of available organisations
* `vcloud_director.get_pvdcs` - Retrieve details about the Provider VDCs

