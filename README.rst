########
Overview
########

This NApp is responsible for discovering and updating all links in the network.
It can manage links between datapaths themselves or between end-hosts and
datapaths. This application depends on **of_lldp**: it makes use of LLDP
packets to discover links between network devices and mark interfaces as NNIs
(Network to Network Interfaces). As the NApp name suggests, all topology
information is collected using the OpenFlow protocol.

##########
Installing
##########

All of the Kytos Network Applications are located in the NApps online
repository. To install this NApp, run:

.. code:: shell

   $ kytos napps install kytos/of_topology

If you are going to install kytos-napps from source code, all napps will be
installed by default (just remember you need to enable the ones you want
running).

######
EVENTS
######

********
Listened
********

kytos/of_core.v0x0[14].messages.in.ofpt_packet_in
=================================================
PacketIn events are analyzed to look for end hosts in the topology. As
**of_lldp** discovers links between switches, **of_topology** ignores LLDP
packets, making use of any other message coming from a UNI (User to Network
Interface to update information about the host connected at the other end.

kytos/of_core.v0x0[14].messages.in.ofpt_port_status
===================================================
Everytime a datapath sends a PortStatus reporting a change, **of_topology**
replicates the changes in the topology, deleting ports marked as removed and
updating the status (up/down) everytime it is modified. Independent of the
PortStatus reason, an event is generated to notify other NApps of the topology
change.

*********
Generated
*********

kytos/of_topology.change.port.down
==================================
Event sent by **of_topology** when a datapath sends a PortStatus reporting that
a port was removed or disabled. The event is an instance of KytosEvent, with
the following data:

.. code-block:: python3

   content = { reason:['disabled' | 'removed'],
               dpid: <switch.dpid>,
               port_description: {<description of the port>}
             }

kytos/of_topology.change.port.up
================================

Event sent by **of_topology** when a datapath sends a PortStatus reporting that
a port was created or enabled is an instance of `KytosEvent` class with the
following content:

.. code-block:: python3

   content = { reason:['enabled' | 'created'],
               dpid: <switch.dpid>,
               port_description: {<description of the port>}
             }
