# Rules
The rules folder contains rules. See [Rules](http://docs.stackstorm.com/rules.html) for specifics on writing rules.

----------

Example rule [`parse_message.yaml`](parse_message.yaml) with criteria filters based on received message from Kafka.

`KafkaMessageSensor` listens to `test` topic (see [config.yaml](./../config.yaml)) of `localhost:9092`
Kafka host and when new message appears, it emits `kafka.new_message` trigger into StackStorm engine.
Additionally sensor detects if received message is JSON and converts it to object,
to reuse in st2 rules/workflows with filters and criteria. 

##### 1. Install this pack
```sh
st2 run packs.install packs=kafka repo_url=stackstorm/st2-kafka subtree=true
st2ctl reload --register-all
```

##### 2. Enable `parse_message` rule
```sh
st2 rule enable kafka.parse_message
```

##### 3. Publish example JSON-formatted message to `test` topic on default `localhost:9092` Kafka host:
```sh
st2 run kafka.produce topic=test message='{"command": "MONITOR",	"source": "HailATaxii.STIX.dShield.list",	"id": "openz2-123abcde-7641-4169-8227-3584521e1e32", "groupid": "123abcde-7641-4169-8227-3584521e1e32", "timestamp": "2015-07-16T00:00:00Z", "attributeQualification": "ALL",	"attributes": [{"attributeName": "SUBNET", "attributeValue": "99.99.99.0/24"}]}'
```

##### 4. Verify that action from rule was executed:
```sh
st2 execution list --action core.local -n 5
```
