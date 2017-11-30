import socket
import logging

from st2common.runners.base_action import Action
from logging.handlers import SysLogHandler

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class WriteSyslogAction(Action):

    def run(self, message, facility, priority):

        host = self.config['server']
        port = self.config['port']
        protocol = self.config['protocol']

        syslog_proto = {
            "tcp": socket.SOCK_STREAM,
            "udp": socket.SOCK_DGRAM
        }.get(protocol.lower(), "udp")

        handler = SysLogHandler(
            address=(host, port),
            facility=SysLogHandler.facility_names.get(facility, "user"),
            socktype=syslog_proto
        )
        formatter = logging.Formatter('%(module)s[%(process)d]: %(message)s')
        handler.setFormatter(formatter)
        handler.encodePriority(facility, priority)
        log.addHandler(handler)

        log.info(message)
