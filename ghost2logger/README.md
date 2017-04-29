# Ghost2logger README

This is a new pack for StackStorm that does something simple but powerful.

Users send their device and software generated syslogs to a service that is part of this pack.
When rules are created relating to the 'Ghost2logger' syslog pack (this pack!), then those rules are injected into the Ghost2logger syslog service. Through regular expression pattern matching, syslogs that are received are compared against an in memory database. If the transmission host IP address and the regular expression find a match, a trigger is dispatched containing three things:

*	trigger.message
*	trigger.pattern
*	trigger.host

Your actions can then use the trigger fields like any other pack.

Note: StackStorm itself is not acting as the parser for messages. Only messages that have been parsed and matched by the Ghost2logger service are passed in to StackStorm. In essence it's a double match with only 'direct hits' reaching the StackStorm rule engine.

# To install

```st2 pack install https://github.com/DavidJohnGee/ghost2loggeralpha```

Create an ST2 API-Token

```st2 apikey create -k -m '{"used_by": "Ghost2logger"}'```

When the token is generated, make a note of it.

Configure the Ghost2logger pack

```st2 pack config ghost2logger```

You can accept the defaults barring the apikey.

This ```config.yaml``` which lives in the StackStorm ```/opt/stackstorm/configs``` directory is nearly all defaults. Remember, change the ```st2_api_key``` to the one just generated.

```yaml
---
  username: "admin"
  password: "admin"
  st2_api_key: "ODQzNmU3ZWVhNWNiYmQ1NTllZTNmMDc3NjkzZDE3ZjRiMDNhODQyMDE3YzlmYzA2MjVjNDE0YWU4NGJhNDhmMg"
  syslog_listen_port: "514"
  sensor_listen_ip: "0.0.0.0"
  sensor_listen_port: "12022"
  ghost_ip: "0.0.0.0"
  ghost_port: "12023"
  st2url: "http://127.0.0.1:9101/v1/rules/?limit=10&pack=ghost2logger"
```

# Ghost2logger Service

As the Ghost2logger component is written in Golang (hence the name - Go ST2 Logger - Ghost looks far cooler), we can run the binary in one of two ways:

*	In the foreground under 'screen'. Start the service running then dettach
or run as a service:
*	Copy the /opt/stackstorm/packs/ghost2logger/bin/ghost2logger.service to /etc/systemd/system
	Check that the service can be read: ```systemctl is-active ghost2logger.service```
	Start the service ```systemctl start ghost2logger.service```
	Check that it's running ```systemctl status ghost2logger.service```

	Then you can look at messages coming out of it using: ```journalctl -u ghost2logger.service -f```
  Use Ctrl+c to exit.

# Rules

In order to use Ghost2logger, all you need to do is two things:

*	Point your Syslog senders to the StackStorm instance and port 514
*	Create rules that look like the following:

```yaml
name: rule_1
pack: ghost2logger
ref: ghost2logger.rule_1
criteria:
    trigger.host:
        pattern: 192.168.16.1
        type: eq
    trigger.pattern:
        pattern: thing [0-9]$
        type: eq
enabled: true
tags: []
trigger:
    parameters:
    ref: ghost2logger.pattern_match
    type: ghost2logger.pattern_match
type:
    parameters:
    ref: standard
uid: rule:ghost2logger:rule_1
action:
    parameters:
        channel: '#general'
        message: 'Bot here, I''ve got some news!


            Message: {{trigger.message}}

            Pattern:    {{trigger.pattern}}

            Host:        {{trigger.host}}'
    ref: chatops.post_message
```

In the criteria section of the rule, ensure that the pattern match types are both eq. The trigger.pattern is actually a regular expression, but that pattern is also read from the rules engine and also sent back to it in the trigger. If you try running a regular expression on the same regular expression, it's a little inception(y) and won't work.

# Last Bit

This is in the alpha stage at the moment. Please use the pack in non-critical scenarios until I'm happy it's ready for production.

I'll continue working on it in the background and honing it's abilities.

[Email me](mailto:david.gee@ipengineer.net) for more information or if you want to contribute.
You can also check [this link](https://www.youtube.com/watch?v=JnxoNuIs2hE) out which shows the Ghost2logger pack working!


