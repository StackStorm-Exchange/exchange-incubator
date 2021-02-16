# IBM Maximo Monitor Ingest Pack

This pack uses Maximo Monitor SDK (https://github.com/ibm-watson-iot/maximo-asset-monitor-sdk.git) in StackStorm dynamically. It has following features:

- Create Entities in Maximo Assset Monitor
- Add Constants, Dimensions and Functions
- Cleaning the CSV data files as per a valid schema
- Load metrics data from a CSV to Maximo

# <a name="QuickStart"></a> Quick Start
## Prerequisites

IBM monitor Ingest pack,
IBM Cloud Access,
IBM Maximo Analytics service Access, Stackstorm,
Python 3.7

## Setup

### Install Monitor Ingest pack on local StackStorm env
1. Clone from Github repo [Monitor Ingest_pack](https://github.ibm.com/Watson-IoT/monitor_ingest):

    ```
    # clone Monitor_Ingest code from github repo
    cd /opt/stackstorm/packs/
    git clone --branch st2 https://github.ibm.com/Watson-IoT/monitor_ingest.git
    ```
## Get credentials
2. Set credentials to connect Watson Analytics Service:
- On the user interface, go to the Services tab.
- Select Watson IoT Platform Analytics and click View Details.
- In the Environment Variables field, click Copy to Clipboard.

## Configuration

3. Copy the example configuration in [monitor_ingest.yaml.example](./monitor_ingest.yaml.example)
to `/opt/stackstorm/configs/monitor_ingest.yaml` and edit as per credentials copied in Step 2.

Config file must have action_type, data_file_path and credentials keys.
To run a specific Actions use `action_type`, `data_file_path` and `credentials` keys.
`action_type` : action type name
`data_file_path` : source json input file for specified action type
`credentials` : Analytics service credentials
 
** Check [config.schema.yaml](./config.schema.yaml) schema before creating your config file.

Example configuration:

```yaml
action_type : "SetupEntityAction | SetupAddConstants | SetupAddDimesions | SetupAddFunctions "
entity_name : ""
data_file_path : "/opt/stackstorm/packs/monitor_ingest/etc/sample_usage_data.json"
credentials:
    _id: "id*******"
    tenantId: "tenant Id"
    db2:
      username: "username"
      password: "pwd"
      databaseName: BLUDB
      port: 50001
      httpsUrl: "https://*******.cloud.ibm.com"
      host: "*******.cloud.ibm.com"
      security: SSL
    iotp:
      url: "https://orgId**.internetofthings.ibmcloud.com/api/v0002"
      orgId: "org Id"
      host: "orgId**.messaging.internetofthings.ibmcloud.com"
      port: 8883
      asHost: "*********.internetofthings.ibmcloud.com"
      apiKey: "api_key"
      apiToken: "api_token"
    messageHub:
      brokers:
      - broker-0-****************************.us-south.eventstreams.cloud.ibm.com:9093
      - broker-1-****************************.us-south.eventstreams.cloud.ibm.com:9093
      - broker-5-****************************.us-south.eventstreams.cloud.ibm.com:9093
      - broker-4-****************************.us-south.eventstreams.cloud.ibm.com:9093
      - broker-2-****************************.us-south.eventstreams.cloud.ibm.com:9093
      - broker-3-****************************.us-south.eventstreams.cloud.ibm.com:9093
      username: "user name"
      password: "password"
    objectStorage:
      region: global
      username: "user name"
      password: "password"
    config:
      objectStorageEndpoint: https://undefined
      bos_logs_bucket: "log bucket"
      bos_runtime_bucket: "runtime bucket"
      mh_topic_analytics_alerts: ''
```

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `sudo st2ctl reload --register-configs`

## Creating Vitual environment in StackStorm (Required only if testing in St2 env)

    ```
    # 1. Setup monitor_ingest Virtual Env in SackStorm 
    st2 run packs.setup_virtualenv packs=monitor_ingest python3=True
    
    # 2. Reload pack actions 
    sudo st2ctl reload --register-all
    
    # 3. Fetch list of installed actions 
    st2 action list -p monitor_ingest
    
    # 4. Run an action
    st2 run <pack.action_name>
    ```

## Actions

The following actions are supported:

### Setup Entity ``setup_entity``
`[Mandatory]`
* To Setup Entity Action use action_type - ``SetupEntityAction``
* To Add Constants to an Entity use action_type - ``SetupAddConstants``
* To Add Dimesions to an Entity use action_type - ``SetupAddDimesions``
* To Add Functions to an Entity use action_type - ``SetupAddFunctions``
* Specify json file path in config -``data_file_path`` 
#### Check /etc directory for Sample data files for Setup Entity Action
* for SetupEntityAction sample [data_file_path](./etc/sample_usage_data.json)
* for SetupAddConstants sample [data_file_path](./etc/sample_constant_data.json)
* for SetupAddDimesions sample [data_file_path](./etc/sample_dimension_data.json)
* for SetupAddFunctions sample [data_file_path](./etc/sample_function_data.json)

### Clean CSV metrics data from a CSV ``clean_csv_data``
`[Mandatory]`
* Specify json Schema file path in config -``json_schema_path``
* Specify csv file path in config -``data_file_path``
#### Check /etc directory for Sample data files for clean_csv_data Action
* for clean_csv_data sample [data_file_path](./etc/sample_csv_data.csv)
* for clean_csv_data sample [json_schema_path](./etc/csvSchema.json)
``Action Output`` - clean and error csv files will be under ./etc/clean_data_output/__.csv

### Data metrics data ingestion using CSV ``csv_data_ingest``
`[Mandatory]`
* Specify json file path in config -``data_file_path``
* Specify entity name in config - ``entity_name``
#### Check /etc directory for Sample data files for csv_data_ingest Action
* for csv_data_ingest [sample data file](./etc/sample_csv_data.csv)
* or for a clean csv please check under ./etc/clean_data_output/


## Workflow 
* Action chain workflow added ``clean_data_ingest_chain``


