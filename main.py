"""Read OF messages and dispatch topology related events about them."""
from kytos.core import KytosEvent, KytosNApp, log
from kytos.core.helpers import listen_to
from pyof.foundation.network_types import Ethernet


class Main(KytosNApp):
    """Translate OF messages into network related events.

    Dispatch events with information related to network topology and
    network reachability.

    It works by listening all PacketIns and PortStatus OpenFlow messages and
    generating events with the content that may be used by other NApps.

    """

    def setup(self):
        """Nothing to setup."""
        pass

    def execute(self):
        """Do nothing, only wait for PacketIn messages."""
        pass

    @listen_to('kytos/of_core.v0x0[14].messages.in.ofpt_packet_in')
    def update_links(self, event):
        """Dispatch 'reacheable.mac' event.

        Listen:
            `kytos/of_core.v0x0[14].messages.in.ofpt_packet_in` (KytosEvent)

        Dispatch:
            `reachable.mac` (KytosEvent):
                { switch : <switch.id>,
                  port: <port.port_no>
                  reachable_mac: <mac_address>
                }

        """
        ethernet = Ethernet()
        ethernet.unpack(event.message.data.value)

        name = 'kytos/of_topology.reachable.mac'
        content = {'switch': event.source.switch.id,
                   'port': event.message.in_port,
                   'reachable_mac': ethernet.source}
        event = KytosEvent(name, content)
        self.controller.buffers.app.put(event)

        msg = 'The MAC %s is reachable from switch/port %s/%s.'
        log.debug(msg, ethernet.source, event.source.switch.id,
                  event.message.in_port)

    @listen_to('kytos/of_core.v0x0[14].messages.in.ofpt_port_status')
    def update_port_status(self, event):
        """Dispatch 'port.[created|modified|deleted]' event.

        Listen:
            `kytos/of_core.v0x0[14].messages.in.ofpt_port_status`

        Dispatch:
            `kytos/of_topology.port.[created|modified|deleted]` (KytosEvent):
                { switch : <switch.id>,
                  port: <port.port_no>
                  port_description: {<description of the port>}
                }

        """
        port_status = event.message
        reason = port_status.reason.value

        name = 'kytos/of_topology.port.' + reason.lower()
        content = {'switch': event.source.id,
                   'port': port_status.desc.port_no,
                   'port_description': vars(port_status.desc)}

        event = KytosEvent(name=name, content=content)
        self.controller.buffers.app.put(event)

        msg = 'The port %s (%s) from switch %s was %s.'
        log.debug(msg, port_status.desc.port_no, event.source.id, reason)

    def shutdown(self):
        """End of the application."""
        log.debug('Shutting down...')
