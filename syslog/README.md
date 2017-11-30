# Syslog Integration Pack

Pack that provides integration with Syslog servers.  This pack was adpated from the chatops pack.
The main idea of the syslog pack is to be able to use the notification feature in StackStorm to
generate logs for executed actions without having to explicitly create log steps in a workflow.

## Actions

* `format_execution_result` - Transform trigger into a message for syslog.
* `write_syslog` - Send a message to a syslog server.
* `log_via_syslog` - Format an execution and send the write the result as a message to syslog.

## Legal

Obligatory kudos to https://icons8.com/ for the icon.
