# Stackstorm-Nexus3

[Sontatype nexus3](https://www.sonatype.com/nexus-repository-oss) stackstorm pack

## Installation


Install this pack with: `st2 pack install file:///$PWD`

Or if in remote repository: `st2 pack install https://github.com/MY/PACK`

## Configuration

Copy the example configuration in [nexus3.yaml.example](./nexus3.yaml.example)
to `/opt/stackstorm/configs/nexus3.yaml` and edit as required.

add nexus3 server connection profile:

* ``url`` - URL of the nexus3 server (e.g. ``http://localhost:8081``)
* ``user`` - username
* ``password`` - Password
* ``verify`` - https tls verify, only used if the `url` option specifies an `https` connection

You can also add multiple profiles:

When you add multiple profile, above parameters becomes defaults for any key missing in the profile.

``` yaml
---
url: "http://localhost:8081"
user: "admin"
password: "admin123"
verify: True
default_profile: "dev"  # use this to make for missing config_profile parameter when calling any action
profiles:
  "dev":
    url: "http://localhost:8081"
    user: "dev-user"
    password: "mypas"
    verify: True
   "dev-2":
     user: "dev2-user"
     password: "mypass2"
     # url : fallback to url: "http://localhost:8081"
     # verify: fallback to verify: True
```


**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`


## Actions

While naming actions following convention is used:

**< VERB >_< RESOURCE(plural) >**


Supported Resources

- Repositories
- Scripts

### Available actions:

* **list_repositories** : List nexus3 repositories
* **get_repositories** : get nexus3 repositories
* **create_repositories** : create nexus3 repository
* **delete_repositories** : delete nexus3 repository

* **list_scripts** : List nexus3 scripts
* **get_scripts** : get nexus3 scripts
* **create_scripts** : create(& upload) if missing, groovy script
* **delete_scripts** : delete nexus3 script

## Policies

* **http.retry** : Retry core.http action on timeout.

## Aliases

--NIL--

## Rules

--NIL--

## Sensors

--NIL--


# Testing


While testing you can leverage [Makefile](./tests/Makefile) to ease writing and testing actions. Read the Makefile for the list of useful commands.


# Contributing

Before submitting make sure python linter is happy with your changes first

```
pip install flake8

#executing flake8 ./
make -f tests/Makefile lint
```