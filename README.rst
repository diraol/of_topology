########
Overview
########

.. attention::

    THIS NAPP IS STILL EXPERIMENTAL AND IT'S EVENTS, METHODS AND STRUCTURES MAY
    CHANGE A LOT ON THE NEXT FEW DAYS/WEEKS, USE IT AT YOUR OWN DISCERNEMENT

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

Content
-------

.. code-block:: python3

    { 'message': <object>,  # instance of a python-openflow PacketIn message
      'source': <object>  # instance of kytos.core.switch.Connection class
    }

kytos/of_core.v0x0[14].messages.in.ofpt_port_status
===================================================
Everytime a datapath sends a PortStatus reporting a change, **of_topology**
replicates the changes in the topology, deleting ports marked as removed and
updating the status (up/down) everytime it is modified. Independent of the
PortStatus reason, an event is generated to notify other NApps of the topology
change.

Content
-------

.. code-block:: python3

    { 'message': <object>,  # instance of a python-openflow PortStatus message
      'source': <object>  # instance of kytos.core.switch.Connection class
    }

*********
Generated
*********

kytos/of_topology.reachable.mac
===============================
Event reporting that a mac address is reachable from a specific switch/port.
This information is retrieved from PacketIns generated sent by the Switches.

Content
-------

.. code-block:: python3

    { 'switch': <switch.id>,  # switch identification
      'port': <port.port_no>,  # port number
      'reachable_mac': <reachable_mac_address>}  # string with mac address

kytos/of_topology.port.created
==============================
Event reporting that a port was created/added in the datapath.
It is dispatched after a PortStatus sent by a datapath is parsed.

Content
-------

.. code-block:: python3

   { 'switch': <switch.id>,  # switch identification
     'port': <port.port_no>,  # port number
     'port_description': {<description of the port>}  # port description dict
   }

kytos/of_topology.port.modified
===============================
Event reporting that a port was modified in the datapath.
It is dispatched after a PortStatus sent by a datapath is parsed.

It worth to say that the PortStatus message just announce that some Port
attributes were modified, but it does not state which one. The event dispatched
will hold all **current** Port attributes. If a NApp needs to know which
attribute was modified, it will need to compare the current list of attributes
with the previous one.

Content
-------

.. code-block:: python3

   { 'switch': <switch.id>,  # switch identification
     'port': <port.port_no>,  # port number
     'port_description': {<description of the port>}  # port description dict
   }

kytos/of_topology.port.deleted
==============================
Event reporting that a port was deleted from the datapath.
It is dispatched after a PortStatus sent by a datapath is parsed.

Content
-------

.. code-block:: python3

   { 'switch': <switch.id>,  # switch identification
     'port_no': <port.port_no>,  # port number
     'port_description': {<description of the port>}  # port description dict
   }
