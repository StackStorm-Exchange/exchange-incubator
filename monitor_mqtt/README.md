# IBM Maximo Monitor Mqtt Pack

Content of pack

- Sensor to listen or subscribe data from a topic
- Action to clean data 
- Action to publish data to a topic
- Action to publish bulk data to monitor
- Rule to filter data ingested to StackStrom


# <a name="QuickStart"></a> Quick Start
## Prerequisites

IBM Watson IOT Service and Stackstorm, and Python3.7 up and running.

## Setup

### Install IBM Maximo Monitor Mqtt pack on local StackStorm env
 Clone from Github repo [IBM Maximo Monitor Mqtt pack](https://github.com/Abhay-Rastogi/monitor_mqtt.git):

    
    # clone monitor_mqtt code from github repo
    git clone --branch st2 https://github.com/Abhay-Rastogi/monitor_mqtt.git
    
### Once pack will be published One can Install from Exchange by pack name
    st2 pack install monitor_mqtt
    

## Configuration

Copy the example configuration in [monitor_mqtt.yaml.example](./monitor_mqtt.yaml.example)
to `/opt/stackstorm/configs/monitor_mqtt.yaml` and edit as required.

* `tenant_id` - Tenant Id
* `hostname` - MQTT Broker to connect to
* `subscribe` - An array of MQTT topics to subscribe to (sensor only)
* `port` - MQTT port to connect to (default: 1883)
* `protocol` - MQTT protocol version (default: MQTTv311)
* `client_id` - Client ID to register on MQTT broker
* `userdata` - Custom userdata to include with each MQTT message payload
* `username` - Username to connect to MQTT Broker
* `password` - Password to connect to MQTT Broker
* `ssl` - Enable SSL support (default: false)
* `ssl_cacert` - Path to SSL CA Certificate
* `ssl_cert` - Path to SSL Certificate
* `ssl_key` - Path to SSL Key
* `data_file_path` - Path of csv file to input for preprocessing 
* `json_schema_path` - Path of json file for validation of data file
* `csvFilePath` - Path of csv file for input to Mqtt Publisher action


`data_file_path` and `json_schema_path` is mandatory to use clean data Action

`csvFilePath` is mandatory to use bulk publish Action

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `sudo st2ctl reload --register-configs`

## Creating Vitual environment in StackStorm (Required only if testing locally)

    
    Setup Monitor Mqtt Virtual Env in SackStorm 
    st2 run packs.setup_virtualenv packs=monitor_mqtt python3=True
    
## Actions

```
Action to clean and process csv data
 st2 run monitor_mqtt.clean_data

Action to publish a message on a topic - monitor_mqtt.publish
 st2 run monitor_mqtt.publish topic="" message=""

Action to publish clean csv data - monitor_mqtt.publishcsvdata
 st2  run monitor_mqtt.publishcsvdata topic=""

Workflow to clean and publish data on a specific topic - monitor_mqtt.clean_data_mqtt_ingest_chain
 st2 run monitor_mqtt.clean_data_mqtt_ingest_chain topic=""
 ```

## Sensor

Connects to a Watson IOT broker, subscribing to various topics and emitting triggers
into the system.

Requires: config setting `subscribe`.
Emits:
  * trigger: monitor_mqtt.message
  * payload: topic, message, userdata, qos, retain
