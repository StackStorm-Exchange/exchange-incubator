# Apache Kafka Integration Pack
This pack allows integration with [Apache Kafka](http://kafka.apache.org/), high-throughput distributed messaging system.

## Actions
* `kafka.produce` - Send *message* categorized by *topic* to Kafka *hosts*.

## Sensors

### KafkaMessageSensor
Connects to a Kafka broker, subscribing to various topics and dispatches triggers for each new message.

When receives new data, it emits:
* trigger: `kafka.new_message`
* payload:
  * `topic` - Category from which message was retrieved (string).
  * `message` - Message. JSON-serialized messages are converted to objects (object|string).
  * `partition` - Topic partition number message belongs to (integer).
  * `offset` - Consumer offset for current topic. Position of what has been consumed (integer).
  * `key` - Message's key, used only for keyed messages (string).

#### Configuration
* `hosts` - Default hosts to send `produce` messages to in host:port format.
            Comma-separated for several hosts. (ex: `localhost:9092`)
* `client_id` - Client ID to send with each message payload (default: `st2-kafka-producer`).
* message_sensor:
  * `hosts` - Kafka hostname(s) to connect in host:port format. Comma-separated for several hosts. (ex: `localhost:9092`)
  * `topics` - Listen for new messages on these topics, (ex: `['test', 'meetings']`)
  * `group_id` - Consumer group (default: `st2-sensor-group`)
  * `client_id` - Client ID to identify application making the request (default: `st2-kafka-consumer`).

## Examples
Send message to Kafka queue:
```sh
# Publish message to `meetings` topic
st2 run kafka.produce topic=meetings message='StackStorm meets Apache Kafka'
# Send JSON-formatted message
st2 run kafka.produce topic=test message='{"menu": {"id": "file"}}'
```
